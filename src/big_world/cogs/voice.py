import os
import time
import discord
from discord.ext import commands
from discord.utils import get

async def is_smert(ctx):
        member = ctx.author
        roles = member.roles
        return 'can_code' in [role.name for role in roles]


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def speak(self, ctx, name=None):
        audio_name = name or "what"
        audio_name += ".mp3"
        member = ctx.author
        if member.voice:
            audio_file_path = os.path.join(os.getcwd(),self.bot.audio,audio_name)
            if os.path.isfile(audio_file_path) and os.path.exists(audio_file_path):
                voice_channel = member.voice.channel
                if self.bot.user not in voice_channel.members:
                    vc = await voice_channel.connect()
                else:
                    vc = self.bot.voice_clients[0]
                vc.play(discord.FFmpegPCMAudio(audio_file_path))
                while vc.is_playing():
                    continue
                await vc.disconnect()
            else:
                audio_not_found = "Sorry, but I haven't learned that phrase yet. You can let zazu know what you want him to teach me. In the meantime check out **!help** to see what I know."
                bot_msg = await ctx.channel.send(audio_not_found)
                time.sleep(8)
                await bot_msg.delete()
        else:
            bot_msg = await ctx.channel.send("How about you join the voice channel and say it yourself 🐔")
            time.sleep(8)
            await bot_msg.delete()
        await ctx.message.delete()
    
    @commands.command()
    @commands.check(is_smert)
    async def learn(self, ctx):
        if ctx.message.attachments:
            attachment = ctx.message.attachments[0]
            audio_file_path = os.path.join(os.getcwd(),self.bot.audio,attachment.filename.lower())
            print("something is happening")
            if attachment.filename[-4:] == '.mp3' and not os.path.exists(audio_file_path):
                print("Something else is happening")
                await attachment.save(audio_file_path)
                print("more stuff")
                await ctx.channel.send(f"I learnded a new phrase, {attachment.filename[0:-4].lower()}")
                print("final stuff")
def setup(bot):
    bot.add_cog(Voice(bot))