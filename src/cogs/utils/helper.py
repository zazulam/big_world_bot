from discord.ext import commands
from discord.utils import get

class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self, ctx):
        pass
    