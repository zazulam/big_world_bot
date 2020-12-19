from discord.ext import commands
from discord.utils import get
from expiringdict import ExpiringDict
from itertools import cycle
import json
import random
import requests

class Poll(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.bot.headcounts = ExpiringDict(max_len=100, max_age_seconds=7200)
        # general gifs to send when an error occurs with the tenor api 
        self.oops_gifs = cycle([
            "https://tenor.com/o4qM.gif",
            "https://tenor.com/rD4V.gif",
            "https://tenor.com/EAAG.gif",
            "https://tenor.com/wKSI.gif",
            "https://tenor.com/1z3x.gif",
            "https://tenor.com/SC5P.gif",
            "https://tenor.com/wI1Z.gif",
            "https://tenor.com/s1N6.gif",
            "https://tenor.com/5mQA.gif",
            "https://tenor.com/Q83q.gif",
            "https://tenor.com/ZKAM.gif",
            "https://tenor.com/bg5z1.gif",
        ])


    @commands.command(description="Ask any question you would like")
    async def poll(self, ctx):
        await ctx.message.add_reaction('👍')
        await ctx.message.add_reaction('👎')
        await ctx.message.add_reaction('🤷')

    @commands.command(description="Request a Among with a number of people i.e. Among Us 9")
    async def headcount(self, ctx, *args):
        game = ' '.join(args)
        poll_request = game.split()
        requested_count = int(poll_request.pop())
        game = ' '.join(poll_request).upper()
        new_content = await self.get_gif(game)
        new_content = "**{}**\n".format(game)+new_content
        bot_msg = await ctx.channel.send(content=new_content)
        await bot_msg.add_reaction('👍')
        await bot_msg.add_reaction('👎')
        await bot_msg.add_reaction('🤷')
        if bot_msg not in self.bot.headcounts:
            self.bot.headcounts[bot_msg.id] = (ctx.author.mention,requested_count,game)
        
    @commands.command(description="Let the bot pull a gif for you by adding some keywords")
    async def gifme(self, ctx, *args):
        if ctx.channel.name != 'all':
            name = ' '.join(args)
            game = name.upper()
            gif = await self.get_gif(game)
            await ctx.channel.send(gif)

    async def get_gif(self, gif_name):
         
        try:
            default_gif = next(self.oops_gifs)
            gif_name = gif_name.replace(" ","+")
            total = 50
            endpoint = "https://api.tenor.com/v1/search?q={}&key={}&limit={}&pos=50".format(gif_name, self.bot.tenor,total)
            r = requests.get(endpoint)
            if r.status_code == 200:
                # return a random gif from the search
                search_list = json.loads(r.content)["results"]
                random_index = random.randint(0,len(search_list)-1)
                random_gif = search_list[random_index]['url']
                default_gif = random_gif
        except Exception as ex:
            print(ex)
        finally:
            return default_gif

def setup(bot):
    bot.add_cog(Poll(bot))