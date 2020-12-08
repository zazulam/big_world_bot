from discord.ext import commands

class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def help(self,):
        pass
    