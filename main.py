import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='.', description='A bot created for the EXID Discord server.')

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('--------')

@bot.command()
async def helloworld(ctx):
    await ctx.send("Hello world!")

bot.run('NDQyMzcwOTQ2MDIwNDA5MzU1.DdFCng.r0OvBdSZZSaJ50m7Vd0dJWLy6qs')