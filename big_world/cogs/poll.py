from discord.ext import commands
from discord.utils import get

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self, ctx):
        pass
    
    @commands.command()
    async def headcount(self, ctx):
        pass
    
    @commands.command()
    async def gifme(self, ctx):
        pass

    async def get_gif(self, ctx):
        pass