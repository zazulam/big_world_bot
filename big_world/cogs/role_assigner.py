from discord.ext import commands
from discord.utils import get

class RoleManager(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def available_roles(self, ctx):
        pass
    
    @commands.command()
    async def role(self, ctx, role_name=None):
        if not role_name:
            await ctx.channel.send("You didn't enter a role, try the command *!roles* for a list of roles you can assign yourself.")
            await ctx.message.delete()
        else:
            role_name = role_name.strip().lower()
            if role_name in self.bot.role_colors:
                role = get(ctx.guild.roles,name=role_name)
                if role:
                    await ctx.author.add_roles(role)
            else:
                await ctx.channel.send("I can't find that role in my list")
