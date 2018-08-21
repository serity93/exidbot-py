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

def setup(bot):
    bot.add_cog(Mod(bot))