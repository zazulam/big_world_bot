from discord.ext import commands
from discord.utils import get

class Sandbox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def python(self, ctx):
        pass

    async def sanitize(self, ctx):
        pass