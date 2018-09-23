import discord
from discord.ext import commands

class Owner:
  def __init__(self, bot):
    self.bot = bot

  @commands.command(
    name='logout',
    description='Shuts down the bot.',
    hidden=True,
    pass_context=True)
  @commands.is_owner()
  async def logout(self, context):
    print('Logging out..!')
    await context.send('Logging out... See ya later!')
    await self.bot.logout()

def setup(bot):
  bot.add_cog(Owner(bot))