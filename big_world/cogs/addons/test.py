import discord
from discord.ext import commands
from discord.utils import get

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def poll(self, ctx):
        await ctx.channel.send("oh so you want a poll ey?")

def setup(bot):
    bot.add_cog(Poll(bot))