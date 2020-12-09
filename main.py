import asyncio
import json
import os
import ast
import random
import time
from collections import deque
from io import StringIO

import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
import requests
import sys
import contextlib
from io import StringIO
import discord
import logging
import text_to_image
from discord.ext import commands
from discord.utils import get
from expiringdict import ExpiringDict
from pptree import *

logging.basicConfig(format='%(asctime)s: %(levelname)s: %(message)s',filename=os.path.join("logs","error.log"),level=logging.ERROR)

with open('config.json','r') as config_file:
    config = json.load(config_file)
intents = discord.Intents.all()
client = discord.Client(intents=intents)
current_invites = {}
role_colors = ['black','cyan','dark green','orange','lime green','white','red','blue','pink','purple','brown','yellow']
colors = []
message_info = {}
headcount_requests = ExpiringDict(max_len=100, max_age_seconds=4800)
invites = {}
last = ""
wildling_code  = "fpnrMdG"


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
    global wildling_code
    await client.wait_until_ready()
    gld = client.get_guild(config["guild_id"])
    channel = gld.text_channels[0]
    print("channel: ",channel)
    while True:
        try:
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
                            wildling_code  = "fpnrMdG"
                            if i.code == wildling_code:
                                await usr.add_roles(role_names['wildling'])
                                embed = discord.Embed(title=f"{usr.name} is now a part of a Big World",description="Watch out! A new wildling has join the server!")
                                inv_mention = i.inviter.mention
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
                tmp.append(tuple((i.code, i.uses)))
            invites = tmp
            await asyncio.sleep(4)
        except Exception as ex:
            logging.error("Error on new joinee",ex,ex.with_traceback())


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
                global role_colors
                global headcount_requests
                global wildling_code
                global message_info
                command = message.content[1:]
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
                        embed.add_field(name="!speak [audio]",value="Bot will join the voice channel that the user is currently in and speak the given audio file, current supported values for audio are: ambulance, believe, bloody, cut, fucked, jerry, out")
                        embed.add_field(name="!poll headcount [game] [count]",value="A poll that will ping the author and all those who react with a :thumbsup: when the count is reach (excluding the bot and author)")
                        embed.add_field(name="!gifme [wOrDz]",value="Have the bot pull a gif of whatever you want, just not in #all")
                        embed.add_field(name="!invite",value="General invite code for the wild.")
                        await message.channel.send(embed=embed)  
                    elif "roles" in command:
                        roles_str = "You can assign the following roles to yourself:\n"
                        for r in role_colors:
                            roles_str = roles_str + r + "\n"
                        await message.channel.send(roles_str)
                    elif command in role_colors:
                        print(member)
                        role = get(member.guild.roles,name=message.content[1:])
                        print("Role:")
                        print(role)
                        name = member.name if member.nick == None else member.nick
                        await member.add_roles(role)
                        await message.channel.send("Congratulations {}, people will now know your favorite Among Us color..hopefully you get to play as it".format(name))
                    elif "sus meter" in command:
                        percentage = round(random.uniform(0,101),2)
                        str_percent = str(percentage)
                        player_name = command.replace('sus meter','').strip()
                        sus_str = ""
                        if player_name.lower() == "3rd imposter":
                            sus_str = "My guy, I'm already SUS AF..I'm apart of the 3 amigos \n( •_•)>⌐■-■\n(⌐■_■)"
                        elif percentage >= 100:
                            sus_str = "👁👄👁 IT'S FUCKING {}, THEIR SUS READING IS {}%".format(player_name,str_percent)
                        elif 90 <= percentage < 100:
                            sus_str = "🚨ALERT!!!🚨 {} has a SUS reading of {}%...should probably vote them in the meeting..".format(player_name,str_percent)
                        elif 80 <= percentage < 90:
                            sus_str = "📈 As you can see by this graph generated by my neural network, {} is clearly SUS with a SUS reading of {}%.".format(player_name,str_percent)
                        elif 20 <= percentage < 80:
                            sus_str = "😐.. Bro, just chill the fuck out and finish your tasks.. {} only had a SUS reading of {}%.".format(player_name,str_percent)
                        else:
                            sus_str = "🤡 It's probably you, {}. {} only barely has any SUS, with just {}%".format(member.name,player_name,str_percent)
                        await message.channel.send(sus_str)             
                    
                    elif "bigworld" in command:
                        G = nx.DiGraph()
                        family = deque()

                        if len(command.split())>1:
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
                        nx.algorithms.coloring.strategy_connected_sequential_bfs(G,None)
                        layout = nx.spring_layout(G,k=4,iterations=50)
                        nx.draw(G,pos=layout, with_labels=True, node_color=colors, node_size=200, node_shape="o", alpha=0.5, linewidths=10, font_size=15,arrowsize=40, font_color="black", font_weight="bold", edge_color="black",cmap=plt.cm.Blues)
                        plt.savefig(f"bigworld_{member.name}.png")
                        await message.channel.send(file=discord.File(f"bigworld_{member.name}.png"))
                        os.remove(f"bigworld_{member.name}.png")         
                    
                    elif "ancestors" in command:
                        if len(command.split())>1:
                            name= command.replace("ancestors","").strip()
                            print(name)
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
                        await message.channel.send(file=discord.File("ancestors_{}.png".format(root_member.name)))
                        
                        os.remove("ancestors_{}.png".format(root_member.name))             

                    elif "family" in command:
                        if len(command.split())>1:
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
                        await message.channel.send(file=discord.File("family_{}.png".format(root_member.name)))
                        
                        os.remove("family_{}.png".format(root_member.name))

                    elif "speak" in command:
                        audio_name = command.split()[-1].lower()+".mp3"
                        print(audio_name)
                        if member.voice:
                            audio_file_path = os.path.join("assets","audio",audio_name)
                            if os.path.isfile(audio_file_path) and os.path.exists(audio_file_path):
                                voice_channel = member.voice.channel
                                if client.user not in voice_channel.members:
                                    vc = await voice_channel.connect()
                                else:
                                    vc = client.voice_clients[0]
                                vc.play(discord.FFmpegPCMAudio(audio_file_path))
                                while vc.is_playing():
                                    continue
                                await vc.disconnect()
                            else:
                                audio_not_found = "Sorry, but I haven't learned that phrase yet. You can let zazu know what you want him to teach me. In the meantime check out **!help** to see what I know."
                                await message.channel.send(audio_not_found)
                        else:
                            await message.channel.send("How about you join the voice channel and say it yourself 🐔")
                        await message.delete()
                    
                    elif "poll" in command:
                        if "headcount" in command.lower():
                            
                            if len(command.split())>2:
                                poll_request = command.split()
                                requested_count = int(poll_request.pop())
                                game = " ".join(poll_request[2:]).upper()
                                new_content = await get_game_gif(game)
                                new_content = "**{}**\n".format(game)+new_content
                                bot_msg = await message.channel.send(content=new_content)
                                await bot_msg.add_reaction('👍')
                                await bot_msg.add_reaction('👎')
                                await bot_msg.add_reaction('🤷')
                                if bot_msg not in headcount_requests:
                                    headcount_requests[bot_msg.id] = (member.mention,requested_count,game)
                        else:
                            await message.add_reaction('👍')
                            await message.add_reaction('👎')
                            await message.add_reaction('🤷')
                        #TODO: Add some flares/updating for when a certain poll is created after hitting a specific number 
                        
                    elif 'gifme' in command:
                        if message.channel.name != 'all':
                            name = command.split()
                            game = " ".join(name[1:]).upper()
                            gif = await get_game_gif(game)
                            await message.channel.send(gif)

                    elif 'invite' in command:
                        wildling_url = "https://discord.gg/{}".format(wildling_code)
                        await message.channel.send(wildling_url)

                    elif 'profile' in command:
                        member_info = {}
                        member_info['joined_at'] = member.joined_at
                        member_info['top_role'] = member.top_role
                        member_info['avatar'] = member.avatar_url
                        member_info['total_messages'] = 0
                        channels = member.guild.text_channels
                        for channel in channels:
                            member_info[channel.name] = 0
                            print("in channel: ",channel.name)
                            async for msg in channel.history(limit=None):
                                if msg.author == member:
                                    member_info[channel.name] += 1
                            member_info['total_messages'] += member_info[channel.name]
                        embed = discord.Embed(title="Server Profile Information",description="Some little statistics/information for {}".format(member.mention),thumbnail=member_info['avatar'])
                        embed.add_field(name="Joined at:", value=member_info['joined_at'])
                        embed.add_field(name="Top Role:",value=member_info['top_role'])
                        embed.add_field(name='Total Messages Sent:',value=member_info['total_messages'])
                        print(member_info)
                        await message.channel.send(embed=embed)
                    
                    elif "msg_load" in command:
                        channels = member.guild.text_channels
                        for mem in member.guild.members:
                            message_info[mem.name] = 0
                        for channel in channels:
                            async for msg in channel.history(limit=None):
                                if msg.author.name in message_info:
                                    message_info[msg.author.name] += 1
                                else:
                                    print(msg.author.name," not in message_info")
                        await message.channel.send(message_info)

                    elif "python" in command:
                        try:
                            formatted_code = command[7:]
                            code = command[11:len(command)-3]
                            ast_node = ast.parse(code)
                            src = ast.dump(ast_node)
                            if 'open' in src:
                                bot_msg = "Idk...this code is a little sus.."
                                await message.channel.send(bot_msg)
                            else:
                                with stdoutIO() as s:
                                    exec(code)
                                bot_msg = formatted_code+"\n**Output:**\n"+s.getvalue()
                                await message.channel.send(bot_msg)
                        except Exception as ex:
                            await message.channel.send(ex)

                    elif "pic" in command:
                        try:
                            member_name = command[3:].strip()
                            member = get(member.guild.members,name=member_name)
                            await message.channel.send(member.avatar_url_as(format='png',size=256))
                        except Exception as ex:
                            print(ex)

                except Exception as ex:
                    logging.error("Error on a bot command: {}".format(command),ex)
                    error_msg = "zazu kinda sucks at coding so he doesn't know how to make me smart enough to handle whatever just happened. 🙄"
                    # await message.channel.send(error_msg)
                finally:
                    colors = []
                    plt.clf()

@contextlib.contextmanager
def stdoutIO(stdout=None):
    old = sys.stdout
    if stdout is None:
        stdout = StringIO()
    sys.stdout = stdout
    yield stdout
    sys.stdout = old

async def get_game_gif(game=None):
    default_gif = "https://tenor.com/view/roll-call-head-count-attendance-name-calling-call-out-gif-15740804"
    
    game.replace(" ","+")
    total = 100
    try:
        endpoint = "https://api.tenor.com/v1/search?q={}&key={}&limit={}".format(game, config['tenor_api_key'],total)
        print(endpoint)
        r = requests.get(endpoint)

        if r.status_code == 200:
            # return a random gif from the search
            search_list = json.loads(r.content)["results"]
            random_index = random.randint(0,len(search_list)-1)
            random_gif = search_list[random_index]['url']
            default_gif = random_gif
    except Exception as ex:
        logging.error("Error occurred while fetching random gif",ex)
    finally:
        return default_gif
        

@client.event
async def on_reaction_add(reaction,member):
    global headcount_requests
    if member.bot:
        return
    if reaction.message.id in headcount_requests:
        if reaction.count-1 >= headcount_requests[reaction.message.id][1]:
            game = headcount_requests[reaction.message.id][2]
            mention = headcount_requests[reaction.message.id][0]
            announcement = "{}, your poll for **{}** has received the requested amount of 👍. Your fellow comrades:\n".format(mention,game)
            comrades = ""
            async for mem in reaction.users():
                if not mem.bot:
                    comrades = comrades + mem.mention+"\n"
            announcement = announcement+comrades
            embed = discord.Embed(title="{} Request".format(game),description="{} your poll has received the desired amount of 👍s.".format(mention))
            embed.add_field(name="Comrades:",value=comrades)
            await reaction.message.channel.send(embed=embed)
            del headcount_requests[reaction.message.id]

@client.event
async def on_member_join(member):
    global last
    last = str(member.id)

if __name__ == "__main__":    
    client.loop.create_task(fetch())
    client.run(config["bot_token"])
