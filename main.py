import asyncio
import json
import os
import random
import sys
import time
from collections import deque
from io import StringIO

import discord
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import text_to_image
from discord.ext import commands
from discord.utils import get
from pptree import *

with open('config.json','r') as config_file:
    config = json.load(config_file)

client = discord.Client()
current_invites = {}

preset_colors = deque(['purple','blue','green','yellow','orange','pink','skyblue','black','brown'])
colors = []
invites = {}
last = ""

async def fetch():
    """
    Steps to auto assign role on new member joining:
    1. Keep track of Server/Guild Invites' uses
    2. When new member joins check Invites for which one had uses increase
    3. Get creator of Invite
    4. Check for Role named after creator
    5. If Role exists named after creator, assign Role to new member
    6. Else create Role then assign to new member
    """
    global last
    global invites
    await client.wait_until_ready()
    gld = client.get_guild(config["guild_id"])
    channel = gld.text_channels[0]
    print("channel: ",channel)
    while True:
        invs = await gld.invites()
        tmp = []
        for i in invs:
            for s in invites:
                if s[0] == i.code:
                    if int(i.uses) > s[1]:
                        usr = gld.get_member(int(last))
                        print("found new member: ",usr.name)
                        roles = gld.roles
                        inviters_role = i.inviter.name
                        print("inviter: ",inviters_role)
                        role_names =  {role.name:role for role in roles}
                        if inviters_role in role_names:
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
        tmp.append(tuple((i.code, i.uses)))
        invites = tmp
        await asyncio.sleep(4)

@client.event
async def on_ready():
    print('logged in as {0.user}'.format(client))
    await client.change_presence(activity = discord.Activity(name = "the vents", type = 2))

@client.event
async def on_message(message):
    print(message.author.name+": "+message.content)
    if message.author == client.user:
        return
    
    member = message.author

    if isinstance(message.content,str):
        if len(message.content) > 0:
            if message.content[0] == "!":
                roles = member.guild.roles
                role_names = [role.name for role in roles[1:13]]
                command = message.content[1:].lower()
                try:
                    global colors
                    if command == "help":
                        embed = discord.Embed(title="Tasks assigned for Bot Imposter:",description="Try out the following commands:")
                        embed.add_field(name="!roles",value="Lists the available roles you can assign to yourself...its just your color")
                        embed.add_field(name="![color]",value="The color you want to assign to youself 🎨")
                        embed.add_field(name="!sus meter [name]",value="sus meter uses bleeding edge AI to determine the SUS levels of a given player")
                        embed.add_field(name="!bigworld [name]", value="Default name is Noonz, shows all the relationships that stem from the name passed")
                        embed.add_field(name="!ancestors [name]", value='Defaults to the person who made the command, shows the lineage tracing from this member all the way up to the First Borne')
                        embed.add_field(name="!family [name]",value="Defaults to the person who made the command, shows the parent and children of the member passed")
                        embed.add_field(name="!poll [question]",value="Added the appropriate reactions for a poll question a user has.")
                        embed.add_field(name="!speak [audio]",value="Bot will join the voice channel that the user is currently in and speak the given audio file, current supported values for audio are: cut, fucked")
                        await message.channel.send(embed=embed)  
                    elif "roles" in command:
                        roles_str = "You can assign the following roles to yourself:\n"
                        for r in role_names:
                            roles_str = roles_str + r + "\n"
                        await message.channel.send(roles_str)
                    elif command in role_names:
                        print(member)
                        role = get(member.guild.roles,name=message.content[1:])
                        print("Role:")
                        print(role)
                        name = member.name if member.nick == None else member.nick
                        await member.add_roles(role)
                        await message.channel.send("Congratulations {}, people will now know your favorite Among Us color..hopefully you get to play as it".format(name))
                    elif "sus meter" in command:
                        percentage = str(round(random.uniform(0,101),2))
                        player_name = command.replace('sus meter','').strip()
                        sus_str = ""
                        if player_name.lower() == "3rd imposter":
                            sus_str = "My guy, I'm already SUS AF..I'm apart of the 3 amigos \n( •_•)>⌐■-■\n(⌐■_■)"
                        elif percentage >= 100:
                            sus_str = "👁👄👁 IT'S FUCKING {}, THEIR SUS READING IS {}%".format(player_name,percentage)
                        elif 90 <= percentage < 100:
                            sus_str = "🚨ALERT!!!🚨 {} has a SUS reading of {}%...should probably vote them in the meeting..".format(player_name,percentage)
                        elif 80 <= percentage < 90:
                            sus_str = "📈 As you can see by this graph generated by my neural network, {} is clearly SUS with a SUS reading of {}%.".format(player_name,percentage)
                        elif 20 <= percentage < 80:
                            sus_str = "😐.. Bro, just chill the fuck out and finish your tasks.. {} only had a SUS reading of {}%.".format(player_name,percentage)
                        else:
                            sus_str = "🤡 It's probably you, {}. {} only barely has any SUS, with just {}%".format(member.name,player_name,percentage)
                        await message.channel.send(sus_str)             
                    elif "bigworld" in command:
                        G = nx.DiGraph()
                        family = deque()

                        if len(command)>8:
                            root_member = get(member.guild.members,name=command.replace("bigworld","").strip())
                            print(root_member)
                        else:
                            root_member = member.guild.owner
                        
                        root_name = root_member.name
                        G.add_node(root_name,image=root_member.avatar_url_as(size=16))
                        curr_color = "red"
                        colors.append(curr_color)
                        root_role = root_name
                        role = get(member.guild.roles,name=root_role)

                        root_node = Node(root_name)
                        family.append(root_node)
                        previous_node = None
                        while len(family)>0:
                            #pop current user/member
                            current_node = family.popleft()
                            curr_member = get(member.guild.members,name=current_node.name)
                            G.add_node(current_node.name,image=curr_member.avatar_url_as(size=16))
                            colors.append("skyblue")
                            print("working on node: {}".format(current_node.name))
                            if current_node.parent:
                                G.add_edge(current_node.parent.name,current_node.name)
                            #get the role associated with said member's name
                            current_role = get(member.guild.roles,name=current_node.name)
                            #search for children assciated with the member's role
                            if current_role:
                                children = current_role.members
                                for child in children:
                                    child_node = Node(child.name,parent=current_node)
                                    print("inserting node: {} into family".format(child.name))
                                    family.append(child_node)
                        colors.pop()
                        res = print_tree(root_node,horizontal=True)
                        nx.algorithms.coloring.strategy_connected_sequential_bfs(G,None)
                        layout = nx.spring_layout(G,k=4,iterations=50)
                        nx.draw(G,pos=layout, with_labels=True, node_color=colors, node_size=200, node_shape="o", alpha=0.5, linewidths=10, font_size=15,arrowsize=40, font_color="black", font_weight="bold", edge_color="black",cmap=plt.cm.Blues)
                        plt.savefig(f"bigworld_{member.name}.png")
                        plt.clf()
                        await message.channel.send(file=discord.File(f"bigworld_{member.name}.png"))
                        colors = []
                        os.remove(f"bigworld_{member.name}.png")         
                    
                    elif "ancestors" in command:
                        if len(command)>9:
                            root_member = get(member.guild.members,name=command.replace("ancestors","").strip())
                            print(root_member)
                        else:
                            root_member = member
                        
                        G = nx.DiGraph()
                        lineage = deque()
                        ancestors = deque()
                        lineage.append(root_member)
                        
                        while len(lineage)>0:
                            member_node = lineage.popleft()
                            possible_ancestors_role = member_node.roles
                            for role in possible_ancestors_role:
                                role_name = role.name
                                print("searching for member: ",role_name)
                                ancestor = get(member.guild.members,name=role_name)
                                if ancestor:
                                    lineage.append(ancestor)
                                    print('lineage: ',lineage)
                                    ancestors.append(member_node)
                                    print('ancestors: ',ancestors)
                            
                            if member_node == member.guild.owner:
                                ancestors.append(member_node)
                        
                        current_node = ancestors.pop()
                        G.add_node(current_node.name)
                        
                        while len(ancestors)>0:
                            next_node = ancestors.pop()
                            print('ancestors: ',ancestors)
                            G.add_node(next_node.name)
                            G.add_edge(current_node.name,next_node.name)
                            current_node = next_node

                        layout = nx.nx.spring_layout(G,k=2,iterations=50)
                        nx.draw(G,pos=layout, with_labels=True,node_size=200, node_shape="o", alpha=0.5, linewidths=10, font_size=15,arrowsize=40, font_color="black", font_weight="bold", edge_color="black",cmap=plt.cm.Blues)
                        plt.savefig("ancestors_{}.png".format(root_member.name))
                        plt.clf()
                        await message.channel.send(file=discord.File("ancestors_{}.png".format(root_member.name)))
                        
                        os.remove("ancestors_{}.png".format(root_member.name))             
                    
                    elif "family" in command:
                        if len(command)>6:
                            root_member = get(member.guild.members,name=command.replace("family","").strip())
                            print(root_member)
                        else:
                            root_member = member

                        G = nx.DiGraph()
                        possible_parent_roles = root_member.roles
                        for role in possible_parent_roles:
                            parent_member = get(member.guild.members,name=role.name)
                            if parent_member:
                                G.add_node(parent_member.name)
                                G.add_node(root_member.name)
                                G.add_edge(parent_member.name,root_member.name)
                        colors.append("skyblue")
                        colors.append("red")
                        root_role = get(member.guild.roles,name=root_member.name)
                        if root_role:
                            children = root_role.members
                            
                            for child in children:
                                G.add_node(child.name)
                                colors.append("skyblue")
                                G.add_edge(root_member.name,child.name)
                        colors = colors[:G.number_of_nodes()]
                        layout = nx.spring_layout(G,k=5,iterations=50)
                        nx.draw(G,pos=layout, with_labels=True, node_color=colors, node_size=200, node_shape="o", alpha=0.5, linewidths=10, font_size=15,arrowsize=40, font_color="black", font_weight="bold", edge_color="black",cmap=plt.cm.Blues)
                        plt.savefig("family_{}.png".format(root_member.name))
                        plt.clf()
                        await message.channel.send(file=discord.File("family_{}.png".format(root_member.name)))
                        
                        os.remove("family_{}.png".format(root_member.name))

                    elif "speak" in command:
                        if member.voice:
                            voice_channel = member.voice.channel
                            if client.user not in voice_channel.members:
                                vc = await voice_channel.connect()
                            else:
                                vc = client.voice_clients[0]
                            if 'fucked' in command:
                                vc.play(discord.FFmpegPCMAudio('fucked_up.mp3'))
                            elif 'cut' in command:
                                vc.play(discord.FFmpegPCMAudio('cut.mp3'))
                            while vc.is_playing():
                                continue
                            await vc.disconnect()
                        else:
                            await message.channel.send("How about you join the voice channel and say it yourself 🐔")
                    
                    elif "poll" in command:
                        await message.add_reaction('👍')
                        await message.add_reaction('👎')
                        await message.add_reaction('🤷')
                        #TODO: Add some flares/updating for when a certain poll is created after hitting a specific number 
                        


                except Exception as ex:
                    print(ex)
                    error_msg   = "zazu kinda sucks at coding so he doesn't know how to make me smart enough to handle whatever just happened. 🙄"
                    await message.channel.send(error_msg)
                finally:
                    colors = []
                    plt.clf()

@client.event
async def on_member_join(member):
    global last
    last = str(member.id)
    await fetch()

client.loop.create_task(fetch())
client.run(config["bot_token"])


