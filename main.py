import constants
import discord
import logging

from discord.ext import commands

bot = commands.Bot(command_prefix='.',
                   description='A bot created for the EXID Discord server.',
                   case_insensitive=True)

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------')

@bot.command()
async def helloworld(ctx):
    await ctx.send("Hello world!")

bot.run(constants.TOKEN)