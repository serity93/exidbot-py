import asyncio
import discord
import io
import json
import logging
import os
import random as rnd
import sys

from constants import *

from apiclient.http import MediaIoBaseDownload
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
from googleapiclient import discovery
from httplib2 import Http
from oauth2client import client, file, tools

# Setup the Drive v3 API
store = file.Storage(CREDENTIALS)
creds = store.get()
if not creds or creds.invalid:
    flow = client.flow_from_clientsecrets(CLIENT_SECRET, SCOPES)
    creds = tools.run_flow(flow, store)
drive_service = discovery.build('drive', 'v3', http=creds.authorize(Http()))

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

################################
## BOT EVENTS
################################

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------')

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

def get_guild_role(role_id, roles):
    for role in roles:
        if role.id == role_id:
            return role

def not_blacklisted(context):
    with open(JSON_DATA_FILE, "r") as file:
        json_data = json.load(file)
    json_roles = json_data['roles']
    guild_roles = context.guild.roles
    
    role = get_guild_role(json_roles['Blacklist']['id'], guild_roles)
    return role not in context.message.author.roles

def user_is_blacklisted(user_roles):
    with open(JSON_DATA_FILE, "r") as file:
        json_data = json.load(file)
    json_roles = json_data['roles']
    blacklist_role = json_roles['Blacklist']

    return blacklist_role in user_roles

async def random_pic(context, pic_q):
    response = {}
    page_token = None
    rnd.seed()

    while True:
        try:
            param = {}
            param['q'] = pic_q
            param['spaces'] = 'drive'
            param['fields'] = 'nextPageToken, files(id, name)'
            param['pageSize'] = 100
            if page_token:
                param['pageToken'] = page_token

            response = drive_service.files().list(**param).execute()
            page_token = response.get('nextPageToken')
            
            if not page_token or rnd.randint(0,100) >= 30:
                break

        except Exception as e:
            print("An error occured: {}".format(e))
            return
    
    pics = response.get('files', [])
    num_pics = len(pics)
    random_pic = pics[rnd.randint(0, num_pics-1)]

    request = drive_service.files().get_media(fileId=random_pic['id'])
    file_name = random_pic['name']
    fh = io.FileIO(random_pic['name'], 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
        status, done = downloader.next_chunk()

    await context.send(file=discord.File(file_name))
    await asyncio.sleep(5)
    fh.close()
    os.remove(file_name)

################################
## MOD COMMANDS
################################

@bot.command(name='exit',
             description='Shuts down the bot.',
             pass_context=True)
@commands.has_role('Mods')
async def exit(context):
    await context.send('See ya!')
    await bot.logout()

################################
## SERVER MEMBER COMMANDS
################################

@bot.command(name='role', pass_context=True)
async def role(context, role_arg):
    if context.message.channel.id == PICK_UR_BIAS_CHAN_ID:
        with open(JSON_DATA_FILE, "r") as file:
            json_data = json.load(file)
        json_roles = json_data['roles']

        member = context.message.author
        roles = context.guild.roles
        message = None

        if role_arg.startswith('-'):
            role_arg = role_arg[1:]
            json_role = json_roles.get(role_arg, None)
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
            json_role = json_roles.get(role_arg, None)
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

@bot.command(name='group',
             description='Posts a random group pic.',
             pass_context=True)
@commands.cooldown(1, 10, BucketType.user)
@commands.check(not_blacklisted)
async def group(context):
    await random_pic(context, GROUP_PIC_Q)

@bot.command(name='solji',
             description='Posts a random Solji pic.',
             aliases=['soulg'],
             pass_context=True)
@commands.cooldown(1, 10, BucketType.user)
@commands.check(not_blacklisted)
async def solji(context):
    await random_pic(context, SOLJI_PIC_Q)

@bot.command(name='le',
             description='Posts a random LE pic.',
             aliases=['hyojin', 'elly'],
             pass_context=True)
@commands.cooldown(1, 10, BucketType.user)
@commands.check(not_blacklisted)
async def le(context):
    await random_pic(context, LE_PIC_Q)

@bot.command(name='hani',
             description='Posts a random Hani pic.',
             aliases=['heeyeon'],
             pass_context=True)
@commands.cooldown(1, 10, BucketType.user)
@commands.check(not_blacklisted)
async def hani(context):
    await random_pic(context, HANI_PIC_Q)

@bot.command(name='hyelin',
             description='Posts a random Hyelin pic.',
             aliases=['hyerin'],
             pass_context=True)
@commands.cooldown(1, 10, BucketType.user)
@commands.check(not_blacklisted)
async def hyelin(context):
    await random_pic(context, HYELIN_PIC_Q)

@bot.command(name='jeonghwa',
             description='Posts a random Jeonghwa pic.',
             aliases=['junghwa'],
             pass_context=True)
@commands.cooldown(1, 10, BucketType.user)
@commands.check(not_blacklisted)
async def jeonghwa(context):
    await random_pic(context, JEONGHWA_PIC_Q)

@bot.command(name='random',
             description='Posts a random EXID pic.',
             pass_context=True)
@commands.cooldown(1, 10, BucketType.user)
@commands.check(not_blacklisted)
async def random(context):
    random_q = ''
    rnd.seed()

    random_int = rnd.randint(1,60)
    if random_int >= 1 and random_int <= 10:
        random_q = GROUP_PIC_Q
    elif random_int >= 11 and random_int <= 20:
        random_q = SOLJI_PIC_Q
    elif random_int >= 21 and random_int <= 30:
        random_q = LE_PIC_Q
    elif random_int >= 31 and random_int <= 40:
        random_q = HANI_PIC_Q
    elif random_int >= 41 and random_int <= 50:
        random_q = HYELIN_PIC_Q
    else:
        random_q = JEONGHWA_PIC_Q

    await random_pic(context, random_q)

bot.run(TOKEN)
