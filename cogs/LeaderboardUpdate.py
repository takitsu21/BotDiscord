import discord,asyncio, datetime, time
from discord.ext import commands
from ressources.leaderboard_database import *

class LeaderboardUpdate(commands.Cog):
    """Update the database leaderboard"""
    def __init__(self, bot):
        self.bot = bot
        self.colour = 0xff0004
        # self.bot.loop.create_task(self.update_leaderboard())

    async def update_leaderboard(self):
        """Update leaderboard every 24 hours"""
        while True:
            try:
                await CreateLeaderboard().leaderboard_to_database()
            except Exception as e:
                print(f'{type(e).__name__} : {e}')
            await asyncio.sleep(86400)

def setup(bot):
    bot.add_cog(LeaderboardUpdate(bot))
    print("Added LeaderboardUpdate Cog from cogs")
