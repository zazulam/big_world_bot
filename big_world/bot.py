from discord.ext import commands

class Bot(commands.Bot):
    def __init__(self, config):
        super().__init__(config.command_prefix,intents=config.intents,description=config.description)
        # self.db = connection
        self.audio = config.audio_resources
        self.image = config.image_resources
        self.tenor = config.tenor_api_key
        self.randoms_code = config.randoms_code
        self.role_colors = config.role_colors
        self.plt_colors = config.plt_colors
        self.sp_client_id = config.spotify['id']
        self.sp_client_secret = config.spotify['secret']
        self.sp_redirect_uri = config.spotify['uri']
        self.sp_scope = config.spotify['scope']
        self.sp_cache = self.image
        self.sp_username = config.spotify['user']
    async def update_wildling_invite(self, new_code):
        self.randoms_code = new_code
        