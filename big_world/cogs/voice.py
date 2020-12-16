import os
import discord
from discord.ext import commands
from discord.utils import get


class Voice(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def speak(self, ctx, name=None):
        audio_name = name or "what"
        audio_name += ".mp3"
        member = ctx.author
        if member.voice:
            print(os.path.join(os.getcwd(),self.bot.config.audio_resources,audio_name))
            print(os.getcwd())
            audio_file_path = os.path.join(os.getcwd(),self.bot.config.audio_resources,audio_name)
            print(os.path.isfile(audio_file_path))
            print(os.path.exists(audio_file_path))
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
                await ctx.channel.send(audio_not_found)
        else:
            await ctx.channel.send("How about you join the voice channel and say it yourself 🐔")
        await ctx.message.delete()

def setup(bot):
    bot.add_cog(Voice(bot))