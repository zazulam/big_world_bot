
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self, command_prefix, description=None):
        super().__init__(command_prefix, description=description)
        

    