from discord.ext import commands
from discord.utils import get

class RoleAssigner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def available_roles(self, ctx):
        pass
    
    @commands.command()
    async def role(self, ctx):
        pass