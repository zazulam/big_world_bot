from discord.ext import commands

class Sandbox(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def python(self,):
        pass

    async def sanitize(self,):
        pass