import discord
from discord.ext import commands

import asyncio
import json

from constants import *
from util import *

class Member:
  def __init__(self, bot):
    self.bot = bot

  @commands.command(name='role', pass_context=True)
  @commands.check(not_blacklisted)
  async def role(self, context, role_arg):
    if context.message.channel.id == PICK_UR_BIAS_CHAN_ID:
      with open(JSON_DATA_FILE, "r") as file:
        json_data = json.load(file)
      json_roles = json_data['roles']

      member = context.author
      message = None

      nugu_role = discord.utils.find(lambda r: r.name == 'Nugu', context.guild.roles)
      leggo_role = discord.utils.find(lambda r: r.name == 'LEGGO', context.guild.roles)

      if role_arg.startswith('-'):
        role_arg = role_arg[1:]
        json_role = json_roles.get(role_arg.lower(), None)
        if json_role is None:
          message = await context.send("Cannot remove the role '" + role_arg + "'! Did you type it correctly?")
        else:
          role_to_remove = discord.utils.find(lambda r: r.id == json_role['id'], context.guild.roles)
          try:
            await member.remove_roles(role_to_remove)
            message = await context.send("Successfully removed the role '" + role_to_remove.name + "'.")
          except Exception:
            message = await context.send("Failed to remove the role '" + role_arg + "'!")      
      elif role_arg.startswith('+'):
        role_arg = role_arg[1:]
        json_role = json_roles.get(role_arg.lower(), None)
        if json_role is None:
          message = await context.send("Cannot add the role '" + role_arg + "'! Did you type it correctly?")
        else:
          role_to_add = discord.utils.find(lambda r: r.id == json_role['id'], context.guild.roles)
          try:
            await member.add_roles(role_to_add)
            await member.add_roles(leggo_role)
            await member.remove_roles(nugu_role)
            message = await context.send("Successfully added the role '" + role_to_add.name + "'.")
          except Exception:
            message = await context.send("Failed to add role '" + role_arg + "'!")
      else:
        message = await context.send("Not sure if you wanted to add or remove '" + role_arg + "'! Add '+/-' at the start of the role name to add/remove the role.")

      await asyncio.sleep(5)
      await context.message.delete()
      await message.delete()

def setup(bot):
  bot.add_cog(Member(bot))