import os
import time
import discord
from discord.ext import commands
from discord.utils import get


class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.quiz_book = set()

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if 'wildling' not in [r.name for r in before.roles] and 'wildling' in [r.name for r in after.roles]:
            time.sleep(3)
            channels = after.guild.text_channels
            channel = [c for c in channels if c.name == f"{after.name.lower()}-test"]
            channel = channel[0]
            embed = discord.Embed(title="Are you ready for your test?",description="Let's see how big brain you are.\nLike this message to start.")
            
            last_msg = await channel.send(embed=embed)
            self.quiz_book.add(last_msg.id)
            await last_msg.add_reaction('👍')

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, member):
        print(reaction.emoji)
        if member.bot:
            return
        if reaction.message.id in self.quiz_book:
            if reaction.emoji == '👍':
                self.quiz_book.add(reaction.message.id)
                embed = discord.Embed(title="Question 1:",description="Was Noonz chasing Evo?")
                embed.add_field(name="A:",value="Yes",inline=True)
                embed.add_field(name="B:",value="No",inline=True)
                embed.add_field(name="C:",value="Who the fuck is Noonz?",inline=True)
                embed.add_field(name="D:",value="Evo saw that cams wasnt on",inline=True)
                last_msg = await reaction.message.channel.send(embed=embed)
                await last_msg.add_reaction('🇦')
                await last_msg.add_reaction('🇧')
                await last_msg.add_reaction('🇨')
                await last_msg.add_reaction('🇩')
                self.quiz_book.add(last_msg.id)
            else:
                role = [r for r in member.roles if r.name == "wildling"]
                await member.remove_roles(role[0])
                await reaction.message.channel.send("That's it! You're correct!\nThis channel will now disappear...")
                time.sleep(8)
                await reaction.message.channel.delete()
                
            
def setup(bot):
    bot.add_cog(Quiz(bot))