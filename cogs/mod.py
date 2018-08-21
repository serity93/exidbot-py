import discord
from discord.ext import commands

class Mod:
  def __init__(self, bot):
        self.bot = bot

  @commands.command(name='say',
    description='Sends a message to the channel.')
  @commands.has_role("Mods")
  async def say(self, context, channel:discord.TextChannel, *, message:str = None):
    if message is None:
      await context.send('Please enter a message for me to send!')
      return

    await context.send(message)
  
  @commands.command(name='announce',
    description='Sends a message in a code block to the channel.')
  @commands.has_role("Mods")
  async def announce(self, context, channel:discord.TextChannel, *, message:str = None):
    if message is None:
      await context.send('Please enter a message for me to send!')
      return

    await context.send('```{}```'.format(message))

  @commands.command(name='mute',
    description='Adds the \'Mute\' role to the member.')
  @commands.has_role("Mods")
  async def mute(self, context, member:discord.Member):
    mute_role = discord.utils.find(lambda r: r.name == 'Mute', context.guild.roles)
    
    try:
      await member.add_roles(mute_role)
      await context.send('Muting **{}**'.format(member.name))
    except Exception as e:
      await context.send('Error when trying to mute **{}**: {}'.format(member.name, e))

  @commands.command(name='unmute',
    description='Removes the \'Mute\' role from the member.')
  @commands.has_role("Mods")
  async def unmute(self, context, member:discord.Member):
    mute_role = discord.utils.find(lambda r: r.name == 'Mute', context.guild.roles)
    
    try:
      await member.remove_roles(mute_role)
      await context.send('Unmuting **{}**'.format(member.name))
    except Exception as e:
      await context.send('Error when trying to unmute **{}**: {}'.format(member.name, e))

  @commands.command(name='kick',
    description='Kicks a member from the server.')
  @commands.has_role("Mods")
  async def kick(self, context, member:discord.Member, *, reason:str = None):
    try:
      await member.kick(reason=reason)
      await context.send('Kicking **{}**'.format(member.name))
    except Exception as e:
      await context.send('Error when trying to kick **{}**: {}'.format(member.name, e))

  @commands.command(name='ban',
    description='Bans a member from the server.')
  @commands.has_role("Mods")
  async def ban(self, context, member:discord.Member, delete_message_days:int = 0, *, reason:str = None):
    try:
      await member.ban(reason=reason, delete_message_days=delete_message_days)
      await context.send('Banning **{}**'.format(member.name))
    except Exception as e:
      await context.send('Error when trying to ban **{}**: {}'.format(member.name, e))

  @commands.command(name='pause',
    description='Disable sending messages to the channel.',
    aliases=['freeze'])
  @commands.has_role("Mods")
  async def pause(self, context):
    everyone_role = context.guild.default_role

    try:
      await context.channel.set_permissions(everyone_role, send_messages=False)
      await context.send('Chat has been disabled.')
    except Exception as e:
      await context.send('Error disabling chat: {}'.format(e))

  @commands.command(name='resume',
    description='Enable sending messages to the channel (deletes overrides).',
    aliases=['unpause', 'unfreeze'])
  @commands.has_role("Mods")
  async def resume(self, context):
    everyone_role = context.guild.default_role

    try:
      await context.channel.set_permissions(everyone_role, overwrite=None)
      await context.send('Chat has been enabled.')
    except Exception as e:
      await context.send('Error enabling chat: {}'.format(e))

def setup(bot):
    bot.add_cog(Mod(bot))