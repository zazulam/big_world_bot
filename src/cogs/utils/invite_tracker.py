from discord.ext import commands

class InviteTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invites = None
        
    @commands.Cog.listener()
    async def on_member_join(self, member):
        pass

    async def track(self):
        pass