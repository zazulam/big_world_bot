from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self, command_prefix, help_command=_default, description=None, **options):
        super().__init__(command_prefix, help_command=help_command, description=description, **options)