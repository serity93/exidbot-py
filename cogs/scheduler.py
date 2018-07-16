import discord
from discord.ext import commands
try:
    from apscheduler.schedulers.asyncio import AsyncIOScheduler
    apscheduler_installed = True
except:
    apscheduler_installed = False
try:
    from apiclient.http import MediaIoBaseDownload
    from googleapiclient import discovery
    from google.oauth2 import service_account
    google_installed = True
except:
    google_installed = False

import asyncio
import datetime
import io
import os
from pytz import utc
import random as rnd

from constants import *

RANDOM_PIC_JOB_ID = 'random_pic_job_id'

class Scheduler:
    def __init__(self, bot):
        self.bot = bot

        self.scheduler = AsyncIOScheduler(timezone=utc)
        self.scheduler.start()

        # Connect to Google Drive API
        credentials = service_account.Credentials.from_service_account_file(
            SERVICE_ACCOUNT, scopes=SCOPES)
        self.drive_service = discovery.build('drive', 'v3', credentials=credentials)

    @commands.group()
    @commands.is_owner()
    async def schedule(self, context):
        if context.invoked_subcommand is None:
            await context.send('Invalid schedule command passed...')

    @schedule.command(
        name='running',
        description='Lists all currently running jobs.',
        pass_context=True)
    async def running(self, context):
        jobs = self.scheduler.get_jobs()

        if not jobs:
            await context.send('There are no currently running jobs.')
            return

        message = '```'
        message += 'JOB ID | NEXT RUN TIME\n\n'
        for job in jobs:
            message += f'{job.id} | {job.next_run_time}\n'
        message += '```'

        await context.send(message)

    @schedule.command(
        name='add',
        description='Adds the job of the given id to the scheduler.')
    async def add(self, context, job_id:str):
        if job_id == RANDOM_PIC_JOB_ID:
            self.add_random_pic_job()
            await context.send(f'Successfully added job with id {RANDOM_PIC_JOB_ID}.')
        else:
            await context.send('Job id not recognized!')

    @schedule.command(
        name='remove',
        description='Removes the job of the given id from the scheduler.')
    async def remove(self, context, job_id:str):
        jobs = self.scheduler.get_jobs()

        for job in jobs:
            if job.id == job_id:
                self.scheduler.remove_job(job_id)
                await context.send(f'Successfully removed job with id {job.id}.')
                return
        
        await context.send(f'There is no job with id {job.id}!')

    def add_random_pic_job(self):
        now = datetime.datetime.now(utc).time()
        midnight = datetime.time(hour=0)
        dawn = datetime.time(hour=6)
        midday = datetime.time(hour=12)
        dusk = datetime.time(hour=18)
        
        start_time = None

        if midnight < now < dawn:
            start_time = datetime.datetime.now(utc).replace(hour=dawn.hour, minute=dawn.minute, second=dawn.second)
        elif dawn < now < midday:
            start_time = datetime.datetime.now(utc).replace(hour=midday.hour, minute=midday.minute, second=midday.second)
        elif midday < now < dusk:
            start_time = datetime.datetime.now(utc).replace(hour=dusk.hour, minute=dusk.minute, second=dusk.second)            
        elif dusk < now:
            start_time = (datetime.datetime.now(utc) + datetime.timedelta(days=1)).replace(hour=midnight.hour, minute=midnight.minute, second=midnight.second)

        self.scheduler.add_job(self.post_random_pic, 'interval', hours=6, next_run_time=start_time, id=RANDOM_PIC_JOB_ID)

    async def post_random_pic(self):
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

        response = {}
        page_token = None
        rnd.seed()

        while True:
            try:
                param = {}
                param['q'] = random_q
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
        random_pic = pics[rnd.randint(0, num_pics-1)]

        request = self.drive_service.files().get_media(fileId=random_pic['id'])
        file_name = random_pic['name']
        fh = io.FileIO(random_pic['name'], 'wb')
        downloader = MediaIoBaseDownload(fh, request)
        done = False
        while done is False:
            status, done = downloader.next_chunk()

        exid_channel = self.bot.get_guild(EXID_GUILD_ID).get_channel(EXID_CHAN_ID)

        await exid_channel.send(file=discord.File(file_name))
        await asyncio.sleep(5)
        fh.close()
        os.remove(file_name)

def setup(bot):
    if not apscheduler_installed:
        raise RuntimeError("You need to run `pip install apscheduler`")
    elif not google_installed:
        raise RuntimeError("You need to run `pip3 install --upgrade google-api-python-client oauth2client`")
    else:
        bot.add_cog(Scheduler(bot))