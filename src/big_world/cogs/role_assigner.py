import time
import discord
from discord.ext import commands
from discord.utils import get

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def available_roles(self, ctx):
        await ctx.channel.send(self.bot.role_colors)
            
    @commands.command()
    async def role_color(self, ctx, role_name=None):
        if not role_name:
            bot_msg = await ctx.channel.send("You didn't enter a role, try the command *!roles* for a list of roles you can assign yourself.")
            await ctx.message.delete()
            time.sleep(5)
            await bot_msg.delete()
        else:
            role_name = role_name.strip().lower()
            if role_name in self.bot.role_colors:
                role = get(ctx.guild.roles,name=role_name)
                if role:
                    await ctx.author.add_roles(role)
            else:
                await ctx.channel.send("I can't find that role in my list")
    
    @commands.has_permissions(manage_roles=True)
    @commands.command()
    async def create_role(self, ctx, role_name=None):
        if not role_name:
            bot_msg = await ctx.channel.send("Please enter a role name")
            time.sleep(5)
            await bot_msg.delete()
        else:
            await ctx.guild.create_role(name=role_name)

def setup(bot):
    bot.add_cog(RoleManager(bot))