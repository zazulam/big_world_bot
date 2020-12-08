from discord.ext import commands

class Metrics(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def stats(self,):
        pass