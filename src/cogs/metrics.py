from discord.ext import commands
from discord.utils import get

class Metrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self, ctx):
        pass