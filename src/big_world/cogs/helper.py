import discord
from discord.ext import commands

class Helper(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command(pass_context=True)
    async def helpme(self, ctx):
        embed = discord.Embed(title="Tasks assigned for Bot Imposter:",description="Try out the following commands:")
        embed.add_field(name="!roles",value="Lists the available roles you can assign to yourself...its just your color")
        embed.add_field(name="![color]",value="The color you want to assign to youself 🎨")
        embed.add_field(name="!sus meter [name]",value="sus meter uses bleeding edge AI to determine the SUS levels of a given player")
        embed.add_field(name="!bigworld [name]", value="Default name is Noonz, shows all the relationships that stem from the name passed")
        embed.add_field(name="!ancestors [name]", value='Defaults to the person who made the command, shows the lineage tracing from this member all the way up to the First Borne')
        embed.add_field(name="!family [name]",value="Defaults to the person who made the command, shows the parent and children of the member passed")
        embed.add_field(name="!poll [question]",value="Added the appropriate reactions for a poll question a user has.")
        embed.add_field(name="!speak [audio]",value="Bot will join the voice channel that the user is currently in and speak the given audio file, current supported values for audio are: ambulance, believe, bloody, cut, fucked, jerry, out")
        embed.add_field(name="!poll headcount [game] [count]",value="A poll that will ping the author and all those who react with a :thumbsup: when the count is reach (excluding the bot and author)")
        embed.add_field(name="!gifme [wOrDz]",value="Have the bot pull a gif of whatever you want, just not in #all")
        embed.add_field(name="!invite",value="General invite code for the wild.")
        await ctx.channel.send(embed=embed)

def setup(bot):
    bot.add_cog(Helper(bot))
    