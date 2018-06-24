import asyncio
import discord
import json
import logging
import os

from constants import *
from discord.ext import commands
from functions import *

# CREATE BOT
bot = commands.Bot(command_prefix='.',
                   description='A bot created for the EXID Discord server.',
                   case_insensitive=True)

# LOGGING
logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)
handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
logger.addHandler(handler)

# DESERIALIZE JSON
with open(JSON_DATA_FILE, "r") as file:
    json_data = json.load(file)

json_roles = json_data['roles']

# EVENTS

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------')

@bot.event
async def on_member_join(member):
    guild = member.guild
    general_channel = guild.get_channel(GENERAL_CHAN_ID)
    roles = guild.roles

    await general_channel.send("Welcome {} to the server! <a:solDanceGif:393867117482737674> Remember to check out {} and {}! LEGGO!"
        .format(member.mention,
        guild.get_channel(WELCOME_CHAN_ID).mention,
        guild.get_channel(PICK_UR_BIAS_CHAN_ID).mention))

    gif = os.path.join(GIF_DIR, WELCOME_GIF)
    await general_channel.send(file=discord.File(gif))

    role = get_guild_role(json_roles['LEGGO']['id'], roles)
    await member.add_roles(role)

@bot.event
async def on_member_remove(member):
    channel = member.guild.get_channel(GENERAL_CHAN_ID)
    await channel.send("**{}** left the server! I hate you for this, can't you feel it? <:JungSad:232632633186713601>"
        .format(member.name))

# COMMANDS

@bot.command(name='role', pass_context=True)
async def role(context, role_arg):
    if context.message.channel.id == PICK_UR_BIAS_CHAN_ID:
        member = context.message.author
        roles = context.guild.roles
        message = None

        if role_arg.startswith('-'):
            role_arg = role_arg[1:]
            json_role = json_roles[role_arg]
            if json_role is None:
                message = await context.send("Cannot remove the role '" + role_arg + "'! Did you type it correctly?")
            else:
                role_to_remove = get_guild_role(json_role['id'], roles)
                try:
                    await member.remove_roles(role_to_remove)
                    message = await context.send("Successfully removed the role '" + role_to_remove.name + "'.")
                except Exception:
                    message = await context.send("Failed to remove the role '" + role_arg + "'!")      
        elif role_arg.startswith('+'):
            role_arg = role_arg[1:]
            json_role = json_roles[role_arg]
            if json_role is None:
                message = await context.send("Cannot add the role '" + role_arg + "'! Did you type it correctly?")
            else:
                role_to_add = get_guild_role(json_role['id'], roles)
                try:
                    await member.add_roles(role_to_add)
                    message = await context.send("Successfully added the role '" + role_to_add.name + "'.")
                except Exception:
                    message = await context.send("Failed to add role '" + role_arg + "'!")
        else:
            message = await context.send("Not sure if you wanted to add or remove '" + role_arg + "'! Add '+/-' at the start of the role name to add/remove the role.")

        await asyncio.sleep(5)
        await context.message.delete()
        await message.delete()

@bot.command(name='solji',
             description='Posts a random Solji pic.',
             aliases=['soulg'],
             pass_context=True)
async def solji(context):
    await context.send('Solji!')

@bot.command(name='le',
             description='Posts a random LE pic.',
             aliases=['hyojin', 'elly'],
             pass_context=True)
async def le(context):
    await context.send('LE!')

@bot.command(name='hani',
             description='Posts a random Hani pic.',
             aliases=['heeyeon'],
             pass_context=True)
async def hani(context):
    await context.send('Hani!')

@bot.command(name='hyelin',
             description='Posts a random Hyelin pic.',
             aliases=['hyerin'],
             pass_context=True)
async def hyelin(context):
    await context.send('Hyelin!')

@bot.command(name='jeonghwa',
             description='Posts a random Jeonghwa pic.',
             aliases=['junghwa'],
             pass_context=True)
async def jeonghwa(context):
    await context.send('Jeonghwa!')

bot.run(TOKEN)
