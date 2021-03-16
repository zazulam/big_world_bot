import boto3
from discord.ext import commands
from discord.utils import get

class Metrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.db = bot.db
    
    @commands.command()
    async def server_stats(self, ctx):
        pass
    
    @commands.command()
    async def user_stats(self,ctx):
        pass

    async def generate_embed(self):
        pass

    async def update_stats(self):
        pass

    