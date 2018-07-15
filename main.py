import discord
from discord.ext import commands

import asyncio
import json
import logging
import os
import traceback
import sys

from constants import *
from bottoken import *
from util import *

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
    'cogs.member',
    'cogs.random_pic'
    ]

# CREATE BOT
bot = commands.Bot(command_prefix=get_prefix,
                   description='A bot created for the EXID Discord server.',
                   case_insensitive=True)

# LOGGING
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
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

################################
## BOT EVENTS
################################

@bot.event
async def on_ready():
    print('\n\n--------')
    print(f'Logged in as: {bot.user.name} - {bot.user.id}\nVersion: {discord.__version__}')
    print('--------\n')

    await bot.change_presence(activity=discord.Activity(name='EXID', type=discord.ActivityType.listening))
    
    print(f'Successfully logged in and booted..!')

@bot.event
async def on_member_join(member):
    with open(JSON_DATA_FILE, "r") as file:
        json_data = json.load(file)
    json_roles = json_data['roles']

    guild = member.guild
    general_channel = guild.get_channel(GENERAL_CHAN_ID)
    roles = guild.roles

    await general_channel.send("Welcome {} to the server! <a:solDanceGif:393867117482737674> Remember to check out {} and {}! LEGGO!"
        .format(member.mention,
        guild.get_channel(WELCOME_CHAN_ID).mention,
        guild.get_channel(PICK_UR_BIAS_CHAN_ID).mention))

    gif = os.path.join(RESOURCES_DIR, WELCOME_GIF)
    await general_channel.send(file=discord.File(gif))

    role = get_guild_role(json_roles['LEGGO']['id'], roles)
    await member.add_roles(role)

@bot.event
async def on_member_remove(member):
    channel = member.guild.get_channel(GENERAL_CHAN_ID)
    await channel.send("**{}** left the server! I hate you for this, can't you feel it? <:JungSad:232632633186713601>"
        .format(member.name))

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return
    elif message.content.startswith('_'):
        await gif_command(message)
    else:
        await bot.process_commands(message)

################################
## FUNCTIONS
################################

def user_is_blacklisted(user_roles):
    with open(JSON_DATA_FILE, "r") as file:
        json_data = json.load(file)
    json_roles = json_data['roles']
    blacklist_role = json_roles['Blacklist']

    return blacklist_role in user_roles

################################
## SERVER MEMBER COMMANDS
################################

#bot.command - post a gif
async def gif_command(message):
    if user_is_blacklisted(message.author.roles):
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

bot.run(TOKEN)
