from big_world.bot import Bot
from big_world.setup.config import Config
from big_world.setup.connector import DBWrapper
import discord
from discord.ext import commands, tasks
import os
from itertools import cycle


def main():
    statuses = cycle(["the vents",
                    "Evo claim Sheriff again",
                    "Steeb's fresh crewmate win",
                    "Tony's big brain",
                    "the screams from electrical",
                    "Noonz trying to recall his tasks",
                    "the medbay scan, visual tasks on bruh",
                    "Shortgod poor defense",
                    "reactor ring while everyone does their tasks",
                    "Zaz's lasts word before he's voted off",
                    "Raven rebuttal",
                    "Eller lie through his teeth",
                    "Nakeds",
                    "Dash kill everyone"
                    ])
    #Initialize config & bot & intents
    intents = discord.Intents.default()
    intents.members = True
    c = Config()
    c.intents = intents
    c.description = "A bot that you may find useful"
    connection = DBWrapper(c.AWS_RESOURCE,c.AWS_REGION)
    b = Bot(c,connection)
    
    b.remove_command("help")
    
    async def can_code(ctx):
        member = ctx.author
        roles = member.roles
        return 'can_code' in [role.name for role in roles]

    @tasks.loop(minutes=10)
    async def change_status():
        await b.change_presence(activity=discord.Activity(name=next(statuses),type=2))
    
    @b.command()
    async def help(ctx):
        embed = discord.Embed(title="Tasks assigned for Bot Imposter:",description="Try out the following commands:")
        embed.add_field(name="!available_roles",value="Lists the available roles you can assign to yourself...its just your color")
        embed.add_field(name="!role_color [color]",value="The color you want to assign to youself 🎨")
        embed.add_field(name="!bigworld [name]", value="Default name is Noonz, shows all the relationships that stem from the name passed")
        embed.add_field(name="!ancestors [name]", value='Defaults to the person who made the command, shows the lineage tracing from this member all the way up to the First Borne')
        embed.add_field(name="!family [name]",value="Defaults to the person who made the command, shows the parent and children of the member passed")
        embed.add_field(name="!poll [question]",value="Added the appropriate reactions for a poll question a user has.")
        embed.add_field(name="!speak [audio]",value="Bot will join the voice channel that the user is currently in and speak the given audio file, current supported values for audio are: ambulance, believe, bloody, cut, fucked, jerry, out")
        embed.add_field(name="!headcount [game] [count]",value="A poll that will ping the author and all those who react with a :thumbsup: when the count is reach (excluding the bot and author)")
        embed.add_field(name="!gifme [wOrDz]",value="Have the bot pull a gif of whatever you want, just not in #all")
        embed.add_field(name="!invite",value="General invite code for the wild.")
        await ctx.channel.send(embed=embed)

    @b.event
    async def on_ready():
        await b.change_presence(activity=discord.Activity(name="the vents and liars",type=2))
        change_status.start()
    @b.command()
    @commands.check(can_code)
    async def load(ctx, extension=""):
        try:
            if ctx.message.attachments:
                extension = "big_world.cogs."+extension
                attachment = ctx.message.attachments[0]
                filename = attachment.filename
                if filename[-3:] == ".py":
                    if ctx.author.id == b.config.creator:
                        cog_path = os.path.join(os.getcwd(),"big_world","cogs",filename)
                        extension += filename[:-3]    
                    else:
                        cog_path = os.path.join(os.getcwd(),"big_world","cogs","addons",filename)
                        extension +=  "addons."+filename[:-3]
                    if os.path.exists(cog_path):
                        await ctx.channel.send("Change your filename")
                    else:
                        file = await attachment.read()
                        with open(cog_path,'wb') as f:
                            f.write(file)
                        
                        b.load_extension(extension)
                        await ctx.channel.send(f"successfully loaded {extension}")
                else:
                    await ctx.channel.send("Only python files can be loaded")
            else:
                if os.path.exists(os.path.join(os.getcwd(),"big_world","cogs",extension+".py")):
                    b.load_extension(f"big_world.cogs.{extension}")
                    await ctx.channel.send(f"successfully loaded {extension}")
                elif os.path.exists(os.path.join(os.getcwd(),"big_world","cogs","addons",extension+".py")):
                    b.load_extension(f"big_world.cogs.addons.{extension}")
                    await ctx.channel.send(f"successfully loaded {extension}")
                else:
                    await ctx.channel.send(f"The extension {extension} does not exist")            
        except Exception as ex:
            await ctx.channel.send(ex)
        
    @b.command()
    @commands.check(can_code)
    async def unload(ctx, extension=""):
        if os.path.exists(os.path.join(os.getcwd(),"big_world","cogs",extension+".py")):
            b.unload_extension(f"big_world.cogs.{extension}")
        elif os.path.exists(os.path.join(os.getcwd(),"big_world","cogs","addons",extension+".py")):
            b.unload_extension(f"big_world.cogs.addons.{extension}")
        else:
            await ctx.channel.send(f"The extension {extension} does not exist")
        
    @b.command()
    @commands.check(can_code)
    async def reload(ctx, extension):
        await unload(ctx, extension)
        await load(ctx, extension)


    b.load_extension("big_world.cogs.invite_tracker")
    b.load_extension("big_world.cogs.poll")
    b.load_extension("big_world.cogs.quizlet")
    b.load_extension("big_world.cogs.relation")
    b.load_extension("big_world.cogs.role_assigner")
    b.load_extension("big_world.cogs.voice")
    b.load_extension("big_world.cogs.spotify")
    b.run(c.bot_token)

if __name__ == '__main__':
    main()
