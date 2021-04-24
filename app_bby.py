from big_world.bot import Bot
from big_world.setup.config import Config
import discord
from discord.utils import *
from discord.ext import commands, tasks
import os
import json
import requests
from itertools import cycle
import boto3
import asyncio

def main():
    #Initialize config & bot & intents
    intents = discord.Intents.default()
    intents.members = True
    c = Config()
    c.intents = intents
    c.description = "A bot that you may find useful"
    #connection = DBWrapper(c.AWS_RESOURCE,c.AWS_REGION)
    b = Bot(c,None)
    b.remove_command("help")
    
    sns = boto3.client('sns',region_name='us-east-1')
    products_names = {'3070':'gpu','3080':'gpu','3090':'gpu','PlayStation 5 Digital Edition':'ps5','PlayStation 5 Console':'ps5'}
    @tasks.loop(seconds=13)
    async def check_products_status():
        #bby skus
        guild = get(b.guilds,id=800158238422728764)
        skus = {3070:6429442,
                3080:6429440,
                3090:6429434,
                'ps5d':6430161,
                'ps5':6426149}
        
        
        baseURL = f"https://api.bestbuy.com/v1/products(sku in({skus[3070]},{skus[3080]},{skus[3090]},{skus['ps5d']},{skus['ps5']}))?apiKey={c.bby_key}&sort=name.asc&show=addToCartUrl,name,salePrice,onlineAvailabilityText,onlineAvailability&format=json"
        response = requests.get(baseURL)
        if response.status_code != 200:
            print(response.status_code)
            print(response.text)
            asyncio.sleep(10)        
        else:
            products = json.loads(response.text)['products']
            await guild.channels[2].send(f"BBY API Products Response:\n{products}")
            for p in products:
                if p['onlineAvailability']:
                    print(f"found a {p['name']}")
                    await guild.channels[1].send(f"found a {p['name']}")
                    for key in list(products_names):
                        if key in p['name']:
                            name = key
                            arn = getattr(c,products_names[key]+'_topic_arn')
                            sns.publish(TopicArn=arn,Message=name+'\n'+p['addToCartUrl'])
                            
                            embed = discord.Embed(title=f"{name}",description="Click the link below to auto add to cart")
                            embed.add_field(name='Add to Cart Link',value=p['addToCartUrl'])
                            del products_names[key]
                            await guild.channels[1].send(embed=embed)
    
    @b.command()
    async def help(ctx):
        embed = discord.Embed(title="Trying to find either a RTX 3070, 3080, 3090, and some ps5s:",description="Im constantly checking inventory, if I find one I'll ping the server")
        await ctx.channel.send(embed=embed)

    @b.event
    async def on_ready():
        await b.change_presence(activity=discord.Activity(name="Bestbuy's warehouse",type=2))
        print('Starting gpu queries')
        check_products_status.start()
    

    b.run(c.gpu_bot_token)

if __name__ == '__main__':
    main()
