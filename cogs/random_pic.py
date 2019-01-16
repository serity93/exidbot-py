import discord
from discord.ext import commands
from discord.ext.commands.cooldowns import BucketType
try:
  from apiclient.http import MediaIoBaseDownload
  from googleapiclient import discovery
  from google.oauth2 import service_account
  google_installed = True
except:
  google_installed = False

import asyncio
import io
import os
import random as rnd

from constants import *
from util import *

class RandomPic:
  def __init__(self, bot):
    self.bot = bot

    # Connect to Google Drive API
    credentials = service_account.Credentials.from_service_account_file(
      SERVICE_ACCOUNT, scopes=SCOPES)
    self.drive_service = discovery.build('drive', 'v3', credentials=credentials)

  @commands.command(name='solji',
        description='Posts a random Solji pic.',
        aliases=['soulg', 'leader'],
        pass_context=True)
  @commands.cooldown(1, 10, BucketType.user)
  @commands.check(not_blacklisted)
  async def solji(self, context):
    await self.random_pic(context, SOLJI_PIC_Q)

  @commands.command(name='soljigif',
        description='Posts a random Solji gif.',
        aliases=['soulggif', 'leadergif'],
        pass_context=True)
  @commands.cooldown(1, 30, BucketType.user)
  @commands.check(not_blacklisted)
  async def soljigif(self, context):
    await self.random_pic(context, SOLJI_GIF_Q)

  @commands.command(name='le',
        description='Posts a random LE pic.',
        aliases=['hyojin', 'elly', 'tom'],
        pass_context=True)
  @commands.cooldown(1, 10, BucketType.user)
  @commands.check(not_blacklisted)
  async def le(self, context):
    await self.random_pic(context, LE_PIC_Q)

  @commands.command(name='legif',
        description='Posts a random LE gif.',
        aliases=['hyojingif', 'ellygif', 'tomgif'],
        pass_context=True)
  @commands.cooldown(1, 30, BucketType.user)
  @commands.check(not_blacklisted)
  async def legif(self, context):
    await self.random_pic(context, LE_GIF_Q)

  @commands.command(name='hani',
        description='Posts a random Hani pic.',
        aliases=['heeyeon'],
        pass_context=True)
  @commands.cooldown(1, 10, BucketType.user)
  @commands.check(not_blacklisted)
  async def hani(self, context):
    await self.random_pic(context, HANI_PIC_Q)

  @commands.command(name='hanigif',
        description='Posts a random Hani gif.',
        aliases=['heeyeongif'],
        pass_context=True)
  @commands.cooldown(1, 30, BucketType.user)
  @commands.check(not_blacklisted)
  async def hanigif(self, context):
    await self.random_pic(context, HANI_GIF_Q)

  @commands.command(name='hyelin',
        description='Posts a random Hyelin pic.',
        aliases=['hyerin', 'jenny'],
        pass_context=True)
  @commands.cooldown(1, 10, BucketType.user)
  @commands.check(not_blacklisted)
  async def hyelin(self, context):
    await self.random_pic(context, HYELIN_PIC_Q)

  @commands.command(name='hyelingif',
        description='Posts a random Hyelin gif.',
        aliases=['hyeringif', 'jennygif'],
        pass_context=True)
  @commands.cooldown(1, 30, BucketType.user)
  @commands.check(not_blacklisted)
  async def hyelingif(self, context):
    await self.random_pic(context, HYELIN_GIF_Q)

  @commands.command(name='jeonghwa',
        description='Posts a random Jeonghwa pic.',
        aliases=['junghwa', 'jerry', 'maknae'],
        pass_context=True)
  @commands.cooldown(1, 10, BucketType.user)
  @commands.check(not_blacklisted)
  async def jeonghwa(self, context):
    await self.random_pic(context, JEONGHWA_PIC_Q)

  @commands.command(name='jeonghwagif',
        description='Posts a random Jeonghwa gif.',
        aliases=['junghwagif', 'jerrygif', 'maknaegif'],
        pass_context=True)
  @commands.cooldown(1, 30, BucketType.user)
  @commands.check(not_blacklisted)
  async def jeonghwagif(self, context):
    await self.random_pic(context, JEONGHWA_GIF_Q)

  @commands.command(name='group',
        description='Posts a random group pic.',
        aliases=['exid'],
        pass_context=True)
  @commands.cooldown(1, 10, BucketType.user)
  @commands.check(not_blacklisted)
  async def group(self, context):
    await self.random_pic(context, GROUP_PIC_Q)

  @commands.command(name='groupgif',
        description='Posts a random group gif.',
        aliases=['exidgif'],
        pass_context=True)
  @commands.cooldown(1, 30, BucketType.user)
  @commands.check(not_blacklisted)
  async def groupgif(self, context):
    await self.random_pic(context, GROUP_GIF_Q)

  @commands.command(name='random',
        description='Posts a random EXID pic.',
        pass_context=True)
  @commands.cooldown(1, 10, BucketType.user)
  @commands.check(not_blacklisted)
  async def random(self, context):
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

    await self.random_pic(context, random_q)

  @commands.command(name='randomgif',
        description='Posts a random EXID gif.',
        pass_context=True)
  @commands.cooldown(1, 30, BucketType.user)
  @commands.check(not_blacklisted)
  async def randomgif(self, context):
    random_q = ''
    rnd.seed()

    random_int = rnd.randint(1,60)
    if random_int >= 1 and random_int <= 10:
      random_q = GROUP_GIF_Q
    elif random_int >= 11 and random_int <= 20:
      random_q = SOLJI_GIF_Q
    elif random_int >= 21 and random_int <= 30:
      random_q = LE_GIF_Q
    elif random_int >= 31 and random_int <= 40:
      random_q = HANI_GIF_Q
    elif random_int >= 41 and random_int <= 50:
      random_q = HYELIN_FOLDER
    else:
      random_q = JEONGHWA_GIF_Q

    await self.random_pic(context, random_q)

  async def random_pic(self, context, pic_q):
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

        response = self.drive_service.files().list(**param).execute()
        page_token = response.get('nextPageToken')
        
        if not page_token or rnd.randint(0,100) >= 30:
          break

      except Exception as e:
        print("An error occured: {}".format(e))
        return
    
    pics = response.get('files', [])
    num_pics = len(pics)

    if num_pics <= 0:
      await context.send('I couldn\'t find what you wanted... I\'m sorry <:JungSad:232632633186713601>')
      return

    random_pic = pics[rnd.randint(0, num_pics-1)]

    request = self.drive_service.files().get_media(fileId=random_pic['id'])
    file_name = random_pic['name']
    fh = io.FileIO(random_pic['name'], 'wb')
    downloader = MediaIoBaseDownload(fh, request)
    done = False
    while done is False:
      status, done = downloader.next_chunk()

    try:
      await context.send(file=discord.File(file_name))
    except discord.HTTPException:
      await context.send('The file was too big for me to post... I\'m sorry <:JungSad:232632633186713601>')

    await asyncio.sleep(5)
    fh.close()
    os.remove(file_name)

  async def on_command_error(self, context, error):
    if hasattr(context.command, 'on_error'):
      return

    ignored = (commands.CommandNotFound, commands.UserInputError)

    error = getattr(error, 'original', error)

    if isinstance(error, ignored):
      return
    elif isinstance(error, commands.CommandOnCooldown):
      await context.send(str(error) + ' <:HaniSquint:302921556282310656>')

def setup(bot):
  if google_installed:
    bot.add_cog(RandomPic(bot))
  else:
    raise RuntimeError("You need to run `pip3 install --upgrade google-api-python-client oauth2client`")