from discord.ext import commands
from discord.utils import get

class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def speak(self, ctx):
        pass