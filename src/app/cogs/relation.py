from collections import deque
import discord
from discord.ext import commands
from discord.utils import get
import os
import matplotlib as mpl
import matplotlib.pyplot as plt
import networkx as nx
from pptree import Node

class Relation(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def bigworld(self, ctx, member: discord.Member = None):
        graph = nx.DiGraph()
        queue = deque()
        colors = []
        guild = ctx.guild
        root_member = member or guild.owner
        root_name = root_member.name

        graph.add_node(root_name,image=root_member.avatar_url_as(size=4))   
        current_color = "red"
        colors.append(current_color)
        role = get(guild.roles,name=root_name)

        root_node = Node(root_name)
        queue.append(root_node)
        prev_node = None

        while queue:
            current_node = queue.popleft()
            current_member = get(guild.members,name=current_node.name)
            graph.add_node(current_node.name,image=current_member.avatar_url_as(size=4))
            colors.append("skyblue")
            if current_node.parent:
                graph.add_edge(current_node.parent.name,current_node.name)
            #get the role associated with said member's name
            current_role = get(guild.roles,name=current_node.name)
            #search for children assciated with the member's role
            if current_role:
                children = current_role.members
                for child in children:
                    child_node = Node(child.name,parent=current_node)
                    queue.append(child_node)
        colors.pop()
        nx.algorithms.coloring.strategy_connected_sequential_bfs(G,None)
        layout = nx.spring_layout(graph,k=4,iterations=50)
        nx.draw(graph,pos=layout, with_labels=True, node_color=colors, node_size=200, node_shape="o", alpha=0.5, linewidths=10, font_size=15,arrowsize=40, font_color="black", font_weight="bold", edge_color="black",cmap=plt.cm.Blues)
        img_path = "bigworld_{}.png".format(root_member.name)
        plt.savefig(img_path)
        await ctx.channel.send(file=discord.File(img_path))
        os.remove(img_path)

    @commands.command()
    async def ancestors(self, ctx, member:discord.Member = None):
        graph = nx.DiGraph()
        lineage = deque()
        ancestors = deque()
        guild = ctx.guild
        root_member = member or guild.owner
        root_name = root_member.name

        lineage.append(root_member)

        while lineage:
            current_node = lineage.popleft()
            possible_ancestors = current_node.roles
            for role in possible_ancestors:
                role_name = role.name
                #search for a member named after said role
                ancestor = get(guild.members,name=role_name)
                if ancestor:
                    lineage.append(ancestor)
                    ancestors.append(current_node)
            
            if current_node == guild.owner:
                ancestors.append(current_node)
            
        current_node = ancestors.pop()
        graph.add_node(current_node.name)

        while ancestors:
            next_node = ancestors.pop()
            graph.add_node(next_node.name)
            graph.add_node(current_node.name,next_node.name)
            current_node = next_node
        
        layout = nx.spring_layout(graph,k=2,iterations=50)
        nx.draw(graph,pos=layout, with_labels=True,node_size=200, node_shape="o", alpha=0.5, linewidths=10, font_size=15,arrowsize=40, font_color="black", font_weight="bold", edge_color="black",cmap=plt.cm.Blues)
        img_path = "ancestors_{}.png".format(root_member.name)
        plt.savefig(img_path)
        await ctx.channel.send(file=discord.File(img_path))
        
        os.remove(img_path)
        
    @commands.command()
    async def family(self, ctx, member:discord.Member = None):
        graph = nx.DiGraph()
        colors = []
        guild = ctx.guild
        root_member = member or guild.owner
        root_name = root_member.name

        possible_parent_roles = root_member.roles
        for role in possible_parent_roles:
            parent_member = get(guild.members,name=role.name)
            if parent_member:
                graph.add_node(parent_member.name)
                graph.add_node(root_member.name)
                graph.add_edge(parent_member.name,root_member.name)
        colors.append("skyblue")
        colors.append("red")
        root_role = get(guild.roles, name=root_member.name)
        if root_role:
            children = root_role.members
            for child in children:
                graph.add_node(child.name)
                colors.append("skyblue")
                graph.add_edge(root_member.name,child.name)
        colors = colors[:graph.number_of_nodes()]
        layout = nx.spring_layout(graph,k=5,iterations=50)
        nx.draw(graph,pos=layout,with_labels=True,node_color=colors,node_size=200, node_shape="o", alpha=0.5, linewidths=10, font_size=15,arrowsize=40, font_color="black", font_weight="bold", edge_color="black",cmap=plt.cm.Blues)
        img_path = "family_{}.png".format(root_member.name)

        plt.savefig(img_path)
        await ctx.channel.send(file=discord.File(img_path))
        
        os.remove("family_{}.png".format(root_member.name))
    
    @commands.command()
    async def lineage(self, ctx, member:discord.Member = None):
        pass
    
    