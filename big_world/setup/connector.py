import boto3

class Connector(object):
    def __init__(self,resource,region):
        self.db = boto3.resource(resource,region)

    async def add_question(self,question,ans1,ans2,ans3,ans4) -> bool:
        pass
    async def get_all_questions(self) -> dict:
        pass
    async def add_member_metric(self,member:discord.Member, metrics:dict) -> bool:
        pass
    