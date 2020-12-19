from big_world.bot import Bot
from big_world.setup.config import Config
# from big_world.setup.connector import Connector
import discord
from discord.ext import commands
import os


def main():
    
    #Initialize config & bot & intents
    intents = discord.Intents.default()
    intents.members = True
    c = Config()
    # connection = Connector(c.AWS_RESOURCE,c.AWS_REGION)
    description = "A bot that you may find useful"
    b = Bot(
        c.command_prefix,
        intents,
        description,
        # connection,
        c.audio_resources,
        c.image_resources,
        c.tenor_api_key,
        c.randoms_code,
        c.role_colors)
    b.remove_command("help")
    async def can_code(ctx):
        member = ctx.author
        roles = member.roles
        return 'can_code' in [role.name for role in roles]

    @b.event
    async def on_ready():
        await b.change_presence(activity=discord.Activity(name="Bits and Bytes",type=2))

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
    b.run(c.bot_token)

if __name__ == '__main__':
    main()
