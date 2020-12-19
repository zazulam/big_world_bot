import discord
from discord.ext import tasks, commands
from discord.utils import get

class InviteTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.command()
    async def invite(self,ctx):
        invites = await ctx.guild.invites()
        randoms_invite = [inv for inv in invites if inv.code == self.bot.randoms_code]
        if randoms_invite:
            await ctx.channel.send(randoms_invite[0].url)

    @commands.Cog.listener('on_ready')
    async def get_invites(self):
        self.guilds = self.bot.guilds
        self.gld_invites = {}
        for gld in self.guilds:
            self.gld_invites[gld] = []
            invs = await gld.invites()
            for inv in invs:
                self.gld_invites[gld].append(inv)
    
    async def is_mod(ctx):
        roles = [r.name for r in ctx.author.roles if r.name == ctx.author.guild.roles[0]]
        return roles

    @commands.check(is_mod)
    @commands.command()
    async def update_randoms_invite(self,ctx):
        invites = await ctx.guild.invites()
        randoms_invite = [inv for inv in invites if inv.code == self.bot.randoms_code]
        if randoms_invite:
            await randoms_invite[0].delete()
            new_randoms_inv = await ctx.channel.create_invite(max_age=0,max_uses=0)
            self.bot.update_randoms_code(new_randoms_inv.code)

    @commands.Cog.listener()
    async def on_member_join(self,member):
        await member.guild.text_channels[0].send(f"My bot is watching you {member.mention}")
        await self.track(member)
    
    @commands.Cog.listener()
    async def on_member_remove(self,member):
        #Get member's roles to check for parent role
        member_roles = member.roles
        parent_role = None
        for role in member_roles:
            possible_parent = get(member.guild.members,name=role.name)
            if possible_parent:
                parent_role = role
                break
        #Get any role named after member to check for children
        children = []
        for mem in member.guild.members:
            mem_roles = mem.roles
            for role in mem_roles:
                if member.name.lower() == role.name:
                    children.append(mem)
                    await mem.remove_roles(role)
        #link the parent role to the children
        if parent_role and children:
            for child in children:
                await child.add_roles(parent_role)
        #Check for any possible test channels and delete them
        name = member.name.strip().lower()
        text_channels = member.guild.text_channels
        member_channel = [t for t in text_channels if t.name == f'{name}-test']
        if member_channel:
            await member_channel[0].delete()

    async def track(self,member=None):
        """
        Steps to auto assign role on new member joining:
        1. Keep track of Server/Guild Invites' uses
        2. When new member joins check Invites for which one had uses increase
        3. Get creator of Invite
        4. Check for Role named after creator
        5. If Role exists named after creator, assign Role to new member
        6. Else create Role then assign to new member
        """        
        randoms_code = self.bot.randoms_code
        await self.bot.wait_until_ready()
        gld = self.bot.get_guild(member.guild.id)
        channel = gld.text_channels[0]
        while True:
            try:
                invs = await gld.invites()
                for i in invs:
                    for s in self.gld_invites[gld]:
                        if s.code == i.code:
                            if int(i.uses) > s.uses:
                                usr = member
                                roles = gld.roles
                                inviters_role = i.inviter.name
                                role_names =  {role.name:role for role in roles}
                                if i.code == randoms_code:
                                   
                                    embed = discord.Embed(title=f"{usr.name} is now a part of a Big World",description="Watch out! A new random has join the server!")
                                    inv_mention = i.inviter.mention
                                    # Create channel specific to user
                                    
                                    overwrites = {
                                        gld.roles[0]:discord.PermissionOverwrite(manage_channels=True,read_messages=True),
                                        role_names['mods']:discord.PermissionOverwrite(manage_channels=True,read_messages=True),
                                        role_names['can_code']:discord.PermissionOverwrite(manage_channels=True,read_messages=True),
                                        gld.default_role: discord.PermissionOverwrite(read_messages=False),
                                        gld.me: discord.PermissionOverwrite(read_messages=True,send_messages=True),
                                        usr: discord.PermissionOverwrite(read_messages=True,send_messages=False)
                                    }
                                    usr_channel = await  gld.create_text_channel(f"{usr.name.lower()}-test",overwrites=overwrites)
                                    await usr.add_roles(role_names['randoms'])
                                    embed.add_field(name="Invited By:",value="Unknown\n Pulling in one from the dark!")
                                    await channel.send(embed=embed)
                                elif inviters_role in role_names:
                                    await usr.add_roles(role_names[inviters_role])
                                    embed = discord.Embed(title=f"{usr.name} is now a part of a Big World",description="good thing you know someone in it 😎")
                                    inv_mention = i.inviter.mention
                                    embed.add_field(name="Invited By:",value=f"{inv_mention} \n Congratulations on the +1!")
                                    await channel.send(embed=embed)
                                else:
                                    new_role = await gld.create_role(name=inviters_role)
                                    await gld.edit_role_positions({new_role:13})
                                    await usr.add_roles(new_role)
                                    embed = discord.Embed(title=f"{usr.name} is now a part of a Big World",description="good thing you know someone in it 😎")
                                    inv_mention = i.inviter.mention
                                    embed.add_field(name=f"Invited By:",value="{} \n Congratulations on the +1!".format(inv_mention))
                                    embed.add_field(name=f"Role:{inviters_role}",value=f"{inv_mention} there is now a role named after you, anyone you invite will be assigned this role.")
                                    await channel.send(embed=embed)
                await self.get_invites()
                break
            except Exception as ex:
                print("Error on new joinee",ex)

def setup(bot):
    i = InviteTracker(bot)
    bot.add_cog(i)
    print("setup executed for invite Tracker")