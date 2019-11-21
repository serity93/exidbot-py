import discord
from discord.ext import commands

import logging
import sys
import traceback

from bottoken import *

"""
A Discord bot written specifically for the EXID Discord server.

Bot owner & main contributor:
  Sean Tyler (sean#0493) (https://github.com/serity93/EXIDbot)

Discord.py Rewrite Documentation:
  http://discordpy.readthedocs.io/en/rewrite/api.html

Discord.py Rewrite Commands Documentation:
  http://discordpy.readthedocs.io/en/rewrite/ext/commands/api.html
"""

def get_prefix(bot, message):
  if not message.guild:
    return '.'

  prefixes = ['.']

  return commands.when_mentioned_or(*prefixes)(bot, message)

initial_extensions = [
  'cogs.owner',
  'cogs.mod',
  'cogs.events',
  #'cogs.json_data',
  'cogs.scheduler',
  'cogs.member',
  'cogs.random_pic',
  ]

# CREATE BOT
bot = commands.Bot(command_prefix=get_prefix,
                   description='A bot created for the EXID Discord server.',
                   case_insensitive=True)

# LOGGING
logger = logging.getLogger('discord')
logger.setLevel(logging.INFO)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

if __name__ == '__main__':
  for extension in initial_extensions:
    try:
      bot.load_extension(extension)
    except Exception as e:
      print(f'Failed to load extension {extension}.', file=sys.stderr)
      traceback.print_exc()

bot.run(TOKEN)