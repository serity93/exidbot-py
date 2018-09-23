import discord
from discord.ext import commands

import os
import random as rnd

from constants import *
from util import *

class Events:
  def __init__(self, bot):
      self.bot = bot

  async def on_ready(self):
    print('\n\n--------')
    print(f'Logged in as: {self.bot.user.name} - {self.bot.user.id}\nVersion: {discord.__version__}')
    print('--------\n')

    await self.bot.change_presence(activity=discord.Activity(name='EXID', type=discord.ActivityType.listening))
    
    print('Successfully logged in and booted..!')

  async def on_member_join(self, member):
    guild = member.guild
    general_channel = guild.get_channel(GENERAL_CHAN_ID)

    await general_channel.send("Welcome {} to the server! <a:solDanceGif:393867117482737674> Please {} to begin chatting and check out {} for more info! LEGGO!"
        .format(member.mention,
        guild.get_channel(PICK_UR_BIAS_CHAN_ID).mention,
        guild.get_channel(WELCOME_CHAN_ID).mention))

    gif = os.path.join(RESOURCES_DIR, WELCOME_GIF)
    await general_channel.send(file=discord.File(gif))

    nugu_role = discord.utils.find(lambda r: r.name == 'Nugu', guild.roles)
    await member.add_roles(nugu_role)

  async def on_member_remove(self, member):
    with open(JSON_DATA_FILE, "r") as file:
        json_data = json.load(file)
    json_messages = json_data['leaveMessages']
    num_msgs = len(json_messages)

    rnd.seed()
    n = rnd.randrange(0, num_msgs)

    channel = member.guild.get_channel(GENERAL_CHAN_ID)
    await channel.send(f"**{member.name}** left the server! " + json_messages[n])

  async def on_message(self, message):
      if message.author == self.bot.user:
          return
      elif message.content.startswith('_'):
          await self.gif_command(message)
      else:
          await self.bot.process_commands(message)
  
  async def gif_command(self, message):
    if user_is_blacklisted(message):
        return

    gif_name = message.content[1:]
    gif_files = os.listdir(GIF_DIR)
    
    if gif_name == 'list':
        list_string = '```'
        for gif_file in gif_files:
            list_string += '_' + gif_file[:-4] + '\n'
        list_string += '```'
        await message.channel.send(content=list_string)
        return

    for gif_file in gif_files:
        if gif_name == gif_file[:-4]:
            gif = os.path.join(GIF_DIR, gif_file)
            await message.channel.send(file=discord.File(gif))
            return

def setup(bot):
  bot.add_cog(Events(bot))