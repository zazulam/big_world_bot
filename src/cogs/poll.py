from discord.ext import commands

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def poll(self,):
        pass
    
    @commands.command()
    async def headcount(self,):
        pass
    
    @commands.command()
    async def gifme(self,):
        pass

    async def get_gif(self,):
        pass