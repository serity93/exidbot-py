import discord
from discord.ext import commands

import os
import random as rnd

from constants import *
from util import *

class Events(commands.Cog):
  def __init__(self, bot):
    self.bot = bot

    self.welcome_messages_channel = None
    self.leave_messages_channel = None
    self.welcome_messages_enabled = True
    self.leave_messages_enabled = True

    self.anti_raid_enabled = False

  #
  # EVENTS
  #

  async def on_ready(self):
    print('\n\n--------')
    print(f'Logged in as: {self.bot.user.name} - {self.bot.user.id}\nVersion: {discord.__version__}')
    print('--------\n')

    await self.bot.change_presence(activity=discord.Activity(name='EXID', type=discord.ActivityType.listening))
    
    print('Successfully logged in and booted..!')

  async def on_member_join(self, member):
    if not self.welcome_messages_enabled:
      return
    
    if self.anti_raid_enabled:
      await self.secure_welcome(member)
    else:
      await self.normal_welcome(member)

  async def on_member_remove(self, member):
    if not self.leave_messages_enabled:
      return

    with open(JSON_DATA_FILE, "r") as file:
      json_data = json.load(file)
    json_messages = json_data['leaveMessages']
    num_msgs = len(json_messages)

    rnd.seed()
    n = rnd.randrange(0, num_msgs)
    message = f"**{member.name}** left the server! " + json_messages[n]
    
    if self.leave_messages_channel is not None:
      await self.leave_messages_channel.send(message)
    else:
      channel = member.guild.get_channel(GENERAL_CHAN_ID)
      await channel.send(message)

  async def on_message(self, message):
    if message.author == self.bot.user:
      return
    elif message.content.startswith('_'):
      await self.gif_command(message)
  
  async def gif_command(self, message):
    if user_is_blacklisted(message):
      return

    gif_name = message.content[1:]
    gif_files = os.listdir(GIF_DIR)
    gif_files.sort()

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
  
  async def normal_welcome(self, member):
    guild = member.guild
    gif = os.path.join(RESOURCES_DIR, WELCOME_GIF)
    message = "Welcome {} to the server! <a:solDanceGif:393867117482737674> Go and {} and check out {} for more info! LEGGO!".format(
      member.mention,
      guild.get_channel(PICK_UR_BIAS_CHAN_ID).mention,
      guild.get_channel(WELCOME_CHAN_ID).mention)
    
    if self.welcome_messages_channel is not None:
      await self.welcome_messages_channel.send(message)
      await self.welcome_messages_channel.send(file=discord.File(gif))
    else:
      general_channel = guild.get_channel(GENERAL_CHAN_ID)
      await general_channel.send(message)
      await general_channel.send(file=discord.File(gif))

    leggo_role = discord.utils.find(lambda r: r.name == 'LEGGO', guild.roles)
    await member.add_roles(leggo_role)
  
  async def secure_welcome(self, member):
    guild = member.guild
    gif = os.path.join(RESOURCES_DIR, WELCOME_GIF)
    message = "Welcome {} to the server! <a:solDanceGif:393867117482737674> Please {} to begin chatting and check out {} for more info! LEGGO!".format(
      member.mention,
      guild.get_channel(PICK_UR_BIAS_CHAN_ID).mention,
      guild.get_channel(WELCOME_CHAN_ID).mention)
    
    if self.welcome_messages_channel is not None:
      await self.welcome_messages_channel.send(message)
      await self.welcome_messages_channel.send(file=discord.File(gif))
    else:
      general_channel = guild.get_channel(GENERAL_CHAN_ID)
      await general_channel.send(message)
      await general_channel.send(file=discord.File(gif))

    nugu_role = discord.utils.find(lambda r: r.name == 'Nugu', guild.roles)
    await member.add_roles(nugu_role)

  #
  # ANTI RAID
  #

  @commands.group()
  @commands.has_role("Mods")
  async def anti_raid(self, context):
    if context.invoked_subcommand is None:
      enabled = "enabled" if self.anti_raid_enabled else "disabled"
      message = "Anti-raid welcome is currently " + enabled
      await context.send(message)

  @anti_raid.command(
    name='enable',
    description='Enable anti-raid welcome',
    aliases=['on'],
    pass_context=True
  )
  async def anti_raid_enable(self, context):
    self.anti_raid_enabled = True
    await context.send("Anti-raid welcome has been enabled!")

  @anti_raid.command(
    name='disable',
    description='Disable anti-raid welcome',
    aliases=['off'],
    pass_context=True
  )
  async def anti_raid_disable(self, context):
    self.anti_raid_enabled = False
    await context.send("Anti-raid welcome has been disabled!")

  #
  # WELCOME MESSAGES
  #

  @commands.group()
  @commands.has_role("Mods")
  async def welcome_messages(self, context):
    if context.invoked_subcommand is None:
      enabled = "enabled" if self.welcome_messages_enabled else "disabled"
      channel = "general (Default)" if self.welcome_messages_channel is None else self.welcome_messages_channel.name
      message = "Welcome messages are " + enabled + "\n" + "Channel: " + channel
      await context.send(message)

  @welcome_messages.command(
    name='enable',
    description='Enable welcome messages',
    aliases=['on'],
    pass_context=True)
  async def welcome_messages_enable(self, context):
    self.welcome_messages_enabled = True
    await context.send("Welcome messages have been enabled!")

  @welcome_messages.command(
    name='disable',
    description='Disable welcome messages',
    aliases=['off'],
    pass_context=True)
  async def welcome_messages_disable(self, context):
    self.welcome_messages_enabled = False
    await context.send("Welcome messages have been disabled!")

  #
  # LEAVE MESSAGES
  #

  @commands.group()
  @commands.has_role("Mods")
  async def leave_messages(self, context):
    if context.invoked_subcommand is None:
      enabled = "enabled" if self.leave_messages_enabled else "disabled"
      channel = "general (Default)" if self.leave_messages_channel is None else self.leave_messages_channel.name
      message = "Leave messages are " + enabled + "\n" + "Channel: " + channel
      await context.send(message)

  @leave_messages.command(
    name='enable',
    description='Enable leave messages',
    aliases=['on'],
    pass_context=True)
  async def leave_messages_enable(self, context):
    self.leave_messages_enabled = True
    await context.send("Leave messages have been enabled!")

  @leave_messages.command(
    name='disable',
    description='Disable leave messages',
    aliases=['off'],
    pass_context=True)
  async def leave_messages_disable(self, context):
    self.leave_messages_enabled = False
    await context.send("Leave messages have been disabled!")

def setup(bot):
  bot.add_cog(Events(bot))