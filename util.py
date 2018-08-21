import discord
import json

from constants import *

def not_blacklisted(context):
    blacklist_role = discord.utils.find(lambda r: r.name == 'Blacklist', context.guild.roles)
    return blacklist_role not in context.message.author.roles

def user_is_blacklisted(user_roles):
    with open(JSON_DATA_FILE, "r") as file:
        json_data = json.load(file)
    json_roles = json_data['roles']
    blacklist_role = json_roles['Blacklist']

    return blacklist_role in user_roles