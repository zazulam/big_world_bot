import discord
from discord.ext import tasks, commands
from discord.utils import get

class InviteTracker(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
    
    @commands.Cog.listener('on_ready')
    async def get_invites(self):
        print("inside get invites")
        self.guilds = self.bot.guilds
        self.gld_invites = {}
        for gld in self.guilds:
            self.gld_invites[gld] = []
            invs = await gld.invites()
            for inv in invs:
                self.gld_invites[gld].append(inv)

    @commands.Cog.listener()
    async def on_member_join(self,member):
        print("on member triggered")
        await member.guild.text_channels[0].send(f"My bot is watching you {member.name}")
        await self.track(member)
    
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
        wildling_code = "PsNABbD83v" # self.bot.wildling_code
        await self.bot.wait_until_ready()
        gld = self.bot.get_guild(member.guild.id)
        channel = gld.text_channels[0]
        print("channel: ",channel)
        while True:
            try:
                invs = await gld.invites()
                for i in invs:
                    for s in self.gld_invites[gld]:
                        if s.code == i.code:
                            if int(i.uses) > s.uses:
                                usr = member
                                print("found new member: ",usr.name)
                                roles = gld.roles
                                inviters_role = i.inviter.name
                                print("inviter: ",inviters_role)
                                role_names =  {role.name:role for role in roles}
                                if i.code == wildling_code:
                                   
                                    embed = discord.Embed(title=f"{usr.name} is now a part of a Big World",description="Watch out! A new wildling has join the server!")
                                    inv_mention = i.inviter.mention
                                    # Create channel specific to user
                                    
                                    overwrites = {
                                        gld.roles[0]:discord.PermissionOverwrite(manage_channels=True,read_messages=True),
                                        gld.default_role: discord.PermissionOverwrite(read_messages=False),
                                        gld.me: discord.PermissionOverwrite(read_messages=True,send_messages=True),
                                        usr: discord.PermissionOverwrite(read_messages=True,send_messages=False)
                                    }
                                    usr_channel = await  gld.create_text_channel(f"{usr.name.lower()}-test",overwrites=overwrites)
                                    await usr.add_roles(role_names['wildling'])
                                    embed.add_field(name="Invited By:",value="The wilderness\n Pulling in one from the dark!")
                                    await channel.send(embed=embed)
                                elif inviters_role in role_names:
                                    print(f"found role for {inviters_role}, adding {inviters_role} role to {usr.name}")
                                    await usr.add_roles(role_names[inviters_role])
                                    print("role successfully added")
                                    embed = discord.Embed(title=f"{usr.name} is now a part of a Big World",description="good thing you know someone in it 😎")
                                    inv_mention = i.inviter.mention
                                    embed.add_field(name="Invited By:",value=f"{inv_mention} \n Congratulations on the +1!")
                                    await channel.send(embed=embed)
                                else:
                                    print(f"role not found for {inviters_role}, creating new role")
                                    new_role = await gld.create_role(name=inviters_role)
                                    await gld.edit_role_positions({new_role:13})
                                    await usr.add_roles(new_role)
                                    print(f"{inviters_role} role successfully created and added to {usr.name}")
                                    embed = discord.Embed(title=f"{usr.name} is now a part of a Big World",description="good thing you know someone in it 😎")
                                    inv_mention = i.inviter.mention
                                    embed.add_field(name=f"Invited By:",value="{} \n Congratulations on the +1!".format(inv_mention))
                                    embed.add_field(name=f"Role:{inviters_role}",value=f"{inv_mention} there is now a role named after you, anyone you invite will be assigned this role.")
                                    await channel.send(embed=embed)
                await self.get_invites()
                break
            except Exception as ex:
                print("Error on new joinee",ex,ex.with_traceback())
def setup(bot):
    i = InviteTracker(bot)
    bot.add_cog(i)
    print("setup executed for invite Tracker")