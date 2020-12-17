
from discord.ext import commands


class Bot(commands.Bot):
    def __init__(self, command_prefix,intents,description,audio_path,image_path,tenor,wildling_code,role_colors):
        super().__init__(command_prefix,intents=intents,description=description)
        self.audio = audio_path
        self.image = image_path
        self.tenor = tenor
        self.wildling_code = wildling_code
        self.role_colors = role_colors

    