import discord
from discord.ext import commands

class Mod:
  def __init__(self, bot):
        self.bot = bot

  @commands.command(name='say')
  async def say(self, context, channel:discord.TextChannel, *, message:str = None):
    if message is None:
      await context.send('Please enter a message for me to send!')
      return

    await context.send(message)
  
  @commands.command(name='announce')
  async def announce(self, context, channel:discord.TextChannel, *, message:str = None):
    if message is None:
      await context.send('Please enter a message for me to send!')
      return

    await context.send('```{}```'.format(message))

  @commands.command(name='mute')
  async def mute(self, context, member:discord.Member):
    mute_role = discord.utils.find(lambda r: r.name == 'Mute', context.guild.roles)
    
    try:
      await member.add_roles(mute_role)
      await context.send('Muting **{}**'.format(member.name))
    except:
      await context.send('Error when trying to mute **{}**!'.format(member.name))

  @commands.command(name='unmute')
  async def unmute(self, context, member:discord.Member):
    mute_role = discord.utils.find(lambda r: r.name == 'Mute', context.guild.roles)
    
    try:
      await member.remove_roles(mute_role)
      await context.send('Unmuting **{}**'.format(member.name))
    except:
      await context.send('Error when trying to unmute **{}**!'.format(member.name))

def setup(bot):
    bot.add_cog(Mod(bot))