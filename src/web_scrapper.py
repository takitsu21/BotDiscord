import re
import unicodedata
from bs4 import BeautifulSoup
from src.utils import _request

user_agent = {'User-Agent':'Mozilla/5.0 (Windows NT x.y; Win64; x64; rv:10.0) Gecko/20100101 Firefox/10.0'}
reddit = 'https://www.reddit.com'
SERVERS = 'https://apexlegendsstatus.com/datacenters'

def checkDaily(a) -> bool: # we don't want daily_discussion
    for c in a.split('/'):
        if re.match(r'^(daily_discussion)\w+',c):
            return False
    return True

def get_subj_title(a) -> str:
    _a = a.split('/')
    return _a[len(_a)-2]

def get_post(categorie) -> str:
    """Returns reddit url filtered by categorie
    -> returns urls filtered"""
    url = f"{reddit}/r/apexlegends/{categorie}"
    content = _request(url, headers=user_agent, call="text")
    page = BeautifulSoup(content, features="lxml")
    reddit_post, check_list = [], []
    for a in page.find_all('a',href=True):
        if a['href'].startswith('/r/apexlegends/comments/') and reddit + a['href'] not in check_list and checkDaily(a['href']):
            check_list.append(reddit + a['href'])
            reddit_post.append('[r/apexlegends/{}]({})\n'.format(get_subj_title(a['href']), reddit + a['href']))
    return '\n'.join(reddit_post)

def get_server_status():
    content = _request(SERVERS, cookies={'lang': 'EN'}, call="text")
    page = BeautifulSoup(content, features="lxml")
    info_server, status = {}, {}
    for i in range(len(page.find_all("div",class_="card-header"))):
        try:
            soup_server = BeautifulSoup(str(page.find_all("div",class_="card-header")[i]), features='lxml')
            server_normalize = unicodedata.normalize("NFKD", soup_server.get_text())
            soup_ms = BeautifulSoup(str(page.find_all("p",class_="card-text")[i]), features='lxml')
            ms_normalize = unicodedata.normalize("NFKD", soup_ms.get_text()).split(' ')[0]
            soup_latency_msg = BeautifulSoup(str(page.find_all("h4", class_="card-title")[i]), features='lxml')
            latency_normalize = unicodedata.normalize("NFKD", soup_latency_msg.get_text())
            if latency_normalize.lower() == 'high latency':
                latency_normalize = '⚠️'
            elif latency_normalize.lower() == 'down':
                latency_normalize = '`❌`'
            else:
                latency_normalize = '✔️'
            info_server['ping'] = ms_normalize
            info_server['latency_msg'] = latency_normalize
            status[server_normalize.lstrip()] = info_server
            info_server = {}
        except Exception as e:
            print(type(e).__name__, e)
    return status

def status() -> str:
    """servers status
    -> returns formatted string about servers for discord"""
    res = ''
    acc = 0
    server_status = get_server_status().items()
    for key, value in server_status:
        old_res = res
        if acc % 2 == 0: # formatting the string output
            res += f"**{key}** : {value['ping']} {value['latency_msg']} | "
        else:
            res += f"**{key}** : {value['ping']} {value['latency_msg']}\n"
        if len(res) >= 2000: # discord raise error when #char > 2000
            return old_res
        acc += 1
    return res

class UnvailableServices(Exception):
    pass

def get_news(limit=6) -> str:
    """Get news from https://www.ea.com/games/apex-legends/news"""
    news_url = "https://www.ea.com/games/apex-legends/news"
    content = _request(news_url, headers=user_agent, call="text")
    page = BeautifulSoup(content, features="lxml")
    news_link = []
    acc = 1
    for c in page.find_all("a", href=True):
        if str(c['href']).startswith('/games/apex-legends/news/') and len(news_link) < limit:
            news_link.append('**#{}** {}{}'.format(acc, "https://www.ea.com",c['href']))
            acc += 1
    return '\n\n'.join(news_link)