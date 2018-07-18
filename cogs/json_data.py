import discord
from discord.ext import commands

import json

from constants import *

LEAVE_MESSAGES = 'leaveMessages'

class JsonData:
    def __init__(self, bot):
        self.bot = bot

    @commands.group()
    @commands.has_role("Mods")
    async def leave_messages(self, context):
        if context.invoked_subcommand is None:
            await context.send(self.list_leave_messages())
    
    def list_leave_messages(self):
        with open(JSON_DATA_FILE, "r") as file:
            json_data = json.load(file)
        json_messages = json_data[LEAVE_MESSAGES]

        output = '```\n'
        index = 0
        for message in json_messages:
            output += f'({index}) {message}\n'
            index += 1
        output += '```'

        return output

def setup(bot):
    bot.add_cog(JsonData(bot))