import discord
from discord.ext import commands

import json

from constants import *

LEAVE_MESSAGES = 'leaveMessages'

class JsonData(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

  @commands.group()
  @commands.has_role("Mods")
  async def leave_messages(self, context):
    if context.invoked_subcommand is None:
      await context.send(self.list_leave_messages())
  
  @leave_messages.command(
    name='add',
    description='Adds a leave message.',
    pass_context=True)
  async def add(self, context, message:str):
    with open(JSON_DATA_FILE, "r") as file:
      json_data = json.load(file)
    json_messages = json_data[LEAVE_MESSAGES]

    json_messages.append(message)
    json_data[LEAVE_MESSAGES] = json_messages

    with open(JSON_DATA_FILE, "w") as outfile:
      json.dump(json_data, outfile)
    
    await context.send(self.list_leave_messages())

  @leave_messages.command(
    name='remove',
    description='Removes a leave message.',
    pass_context=True)
  async def remove(self, context, index:int):
    with open(JSON_DATA_FILE, "r") as file:
      json_data = json.load(file)
    json_messages = json_data[LEAVE_MESSAGES]

    if index < 1 or index > len(json_messages):
      await context.send('Invalid index!')
      return

    json_messages.pop(index-1)
    json_data[LEAVE_MESSAGES] = json_messages

    with open(JSON_DATA_FILE, "w") as outfile:
      json.dump(json_data, outfile)
    
    await context.send(self.list_leave_messages())

  def list_leave_messages(self):
    with open(JSON_DATA_FILE, "r") as file:
      json_data = json.load(file)
    json_messages = json_data[LEAVE_MESSAGES]

    output = '```\n'
    index = 1
    for message in json_messages:
      output += f'({index}) {message}\n'
      index += 1
    output += '```'

    return output

async def setup(bot):
  await bot.add_cog(JsonData(bot))