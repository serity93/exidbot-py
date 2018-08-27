import discord
import json

from constants import *

def not_blacklisted(context):
    blacklist_role = discord.utils.find(lambda r: r.name == 'Blacklist', context.guild.roles)
    return blacklist_role not in context.message.author.roles

def user_is_blacklisted(message):
    blacklist_role = discord.utils.find(lambda r: r.name == 'Blacklist', message.author.guild.roles)
    return blacklist_role in message.author.roles