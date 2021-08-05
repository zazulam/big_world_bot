import boto3

class DBWrapper(object):
    def __init__(self,resource,region):
        self.client = boto3.client(resource,region)

    async def create_table(self, ctx):
        pass

    async def get_item(self,ctx):
        pass

    async def query(self,ctx,criteria):
        pass
    