import discord
from discord.ext import commands
import ressources.web_scrapper as server


class APServer(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.colour = 0xff0004

    @commands.command(pass_context=True)
    async def servers(self,ctx):
        statusServer = await ctx.send('`Checking apexlegendsstatus.com...`')
        try:
            Aps = server.ApexStatus()
            embed = discord.Embed(title='__**Apex Servers Status**__',
                                  description=f'{Aps.status()}',
                                   colour=self.colour)
            embed.set_thumbnail(url=ctx.guild.me.avatar_url)
            embed.set_footer(text="using apexlegendsstatus.com | Made by Taki#0853 (WIP)", icon_url=ctx.guild.me.avatar_url)
            await statusServer.edit(content='',embed = embed)
        except Exception as e:
            embed = discord.Embed(title='__**Apex Servers Status**__', description='[Apex Server Status](https://apexlegendsstatus.com/datacenters)', colour=self.colour)
            embed.set_thumbnail(url=ctx.guild.me.avatar_url)
            embed.set_footer(text="Made by Taki#0853 (WIP)", icon_url=ctx.guild.me.avatar_url)
            print(f'{type(e).__name__} : {e}')
            await statusServer.edit(content='', embed=embed)

def setup(bot):
    bot.add_cog(APServer(bot))
    print("Added APServer cog!")
