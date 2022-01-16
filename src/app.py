from big_world.bot import Bot
from big_world.setup.config import Config
from big_world.setup.connector import DBWrapper
import discord
from discord.ext import commands, tasks
import os
from itertools import cycle

def main():
    #Initialize config & bot & intents
    intents = discord.Intents.default()
    intents.members = True
    c = Config()
    c.intents = intents
    statuses = cycle(c.statuses)
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
    
    @b.event
    async def on_ready():
        await b.change_presence(activity=discord.Activity(name="the inner machinations of my mind",type=2))
        # commenting out for now, until we can obtain user inputs for statuses
        # change_status.start() 
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

    def load_all_cogs():
        for filename in os.listdir(os.path.join(os.getcwd(),"big_world","cogs")):
            if filename[-3:] == ".py":
                b.load_extension(f"big_world.cogs.{filename[:-3]}")
        for filename in os.listdir(os.path.join(os.getcwd(),"big_world","cogs","addons")):
            if filename[-3:] == ".py":
                b.load_extension(f"big_world.cogs.addons.{filename[:-3]}")

    load_all_cogs()
    b.run(c.bot_token)

if __name__ == '__main__':
    main()