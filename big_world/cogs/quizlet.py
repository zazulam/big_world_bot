import os
import time
import discord
from discord.ext import commands
from discord.utils import get


class Quiz(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_update(self, before:discord.Member, after:discord.Member):
        if before.name != after.name:
            #find role of before name and edit to new name to after name
            role = get(before.guild.members,name=before.name.lower())
            if role:
                await role.edit(name=after.name.lower())
        # If the diff between before and after is the Wildling role
        if 'randoms' not in [r.name for r in before.roles] and 'randoms' in [r.name for r in after.roles]:
            # Initialize Quiz for new joinees
            time.sleep(3)
            channels = after.guild.text_channels
            channel = [c for c in channels if c.name == f"{after.name.lower()}-test"]
            if channels:
                channel = channel[0]
                embed = discord.Embed(title="Are you ready for your test?",description="Let's see how big brain you are.\nLike this message to start.")
                
                last_msg = await channel.send(embed=embed)
                await last_msg.add_reaction('👍')
        

    @commands.Cog.listener()
    async def on_reaction_add(self, reaction, member):
        if member.bot:
            return
        if reaction.message.channel.name == f"{member.name.lower()}-test":
            if reaction.emoji == '👍':
                embed = discord.Embed(title="Question 1:",description="Don't be a dick/asshole please")
                embed.add_field(name="A:",value="Yes",inline=True)
                embed.add_field(name="B:",value="No",inline=True)
                embed.add_field(name="C:",value="This isn't a question?",inline=True)
                embed.add_field(name="D:",value="🥴",inline=True)
                last_msg = await reaction.message.channel.send(embed=embed)
                await last_msg.add_reaction('🇦')
                await last_msg.add_reaction('🇧')
                await last_msg.add_reaction('🇨')
                await last_msg.add_reaction('🇩')
            else:
                role = [r for r in member.roles if r.name == "randoms"]

                await member.remove_roles(role[0])
                await 
                await reaction.message.channel.send("That's it! You're correct!\nThis channel will now disappear...")
                time.sleep(5)
                await reaction.message.channel.delete()
        
                
            
def setup(bot):
    bot.add_cog(Quiz(bot))