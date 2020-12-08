from discord.ext import commands

class RoleAssigner(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def available_roles(self,):
        pass
    
    @commands.command()
    async def role(self,):
        pass