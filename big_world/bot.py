from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self, command_prefix,intents,description,audio_path,image_path,tenor,randoms_code,role_colors):
        super().__init__(command_prefix,intents=intents,description=description)
        # self.db = connection
        self.audio = audio_path
        self.image = image_path
        self.tenor = tenor
        self.randoms_code = randoms_code
        self.role_colors = role_colors

    async def update_wildling_invite(self, new_code):
        self.randoms_code = new_code
        #update randoms_code in big_world table