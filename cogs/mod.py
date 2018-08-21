import discord
from discord.ext import commands

class Mod:
  def __init__(self, bot):
        self.bot = bot

  @commands.command(name='say',
    description='Sends a message to the channel.')
  async def say(self, context, channel:discord.TextChannel, *, message:str = None):
    if message is None:
      await context.send('Please enter a message for me to send!')
      return

    await context.send(message)
  
  @commands.command(name='announce',
    description='Sends a message in a code block to the channel.')
  async def announce(self, context, channel:discord.TextChannel, *, message:str = None):
    if message is None:
      await context.send('Please enter a message for me to send!')
      return

    await context.send('```{}```'.format(message))

  @commands.command(name='mute',
    description='Adds the \'Mute\' role to the member.')
  async def mute(self, context, member:discord.Member):
    mute_role = discord.utils.find(lambda r: r.name == 'Mute', context.guild.roles)
    
    try:
      await member.add_roles(mute_role)
      await context.send('Muting **{}**'.format(member.name))
    except Exception as e:
      await context.send('Error when trying to mute **{}**: {}'.format(member.name, e))

  @commands.command(name='unmute',
    description='Removes the \'Mute\' role from the member.')
  async def unmute(self, context, member:discord.Member):
    mute_role = discord.utils.find(lambda r: r.name == 'Mute', context.guild.roles)
    
    try:
      await member.remove_roles(mute_role)
      await context.send('Unmuting **{}**'.format(member.name))
    except Exception as e:
      await context.send('Error when trying to unmute **{}**: {}'.format(member.name, e))

  @commands.command(name='kick',
    description='Kicks a member from the server.')
  async def kick(self, context, member:discord.Member, *, reason:str = None):
    try:
      await member.kick(reason=reason)
      await context.send('Kicking **{}**'.format(member.name))
    except Exception as e:
      await context.send('Error when trying to kick **{}**: {}'.format(member.name, e))

  @commands.command(name='ban',
    description='Bans a member from the server.')
  async def ban(self, context, member:discord.Member, delete_message_days:int = 0, *, reason:str = None):
    try:
      await member.ban(reason=reason, delete_message_days=delete_message_days)
      await context.send('Banning **{}**'.format(member.name))
    except Exception as e:
      await context.send('Error when trying to ban **{}**: {}'.format(member.name, e))

def setup(bot):
    bot.add_cog(Mod(bot))