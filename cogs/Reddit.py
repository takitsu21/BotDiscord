import discord
from discord.ext import commands
import ressources.web_scrapper as scrap_data

colour = 0xc8db

class Reddit(commands.Cog):
    def __init__(self,bot):
        self.bot = bot

    @commands.command(pass_context=True)
    async def reddit(self, ctx, *args):
        try:
            r_args = args[0]
            if r_args == 'hot':
                msg = scrap_data.reddit_post('hot')
            elif r_args == 'top':
                msg = scrap_data.reddit_post('top')
            await ctx.send(msg)
        except Exception as e:
            embed = (discord.Embed(title='Command: !reddit', description='!reddit <hot/top> - Return random recent hot/top on r/apexlegends', colour=colour))
            embed.set_thumbnail(url=ctx.guild.me.avatar_url)
            embed.set_footer(text="Bot created by Taki#0853 (WIP)", icon_url=ctx.guild.me.avatar_url)
            await ctx.send(embed = embed)

def setup(bot):
    bot.add_cog(Reddit(bot))
    print("Added Reddit cog from cogs")
