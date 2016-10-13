from discord.ext import commands
from dateutil.relativedelta import relativedelta

import discord
import datetime
import json
import urllib.request
import os

class Raids:
    def __init__(self, bot):
        self.bot = bot
        self.times = [
            # day, start, end
            [3, [19, 0], [21, 0]],
            [5, [19, 0], [21, 0]],
        ]
        self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    def find_next_raid(self, today):
        raids = []
        for time in self.times:
            next_raid = datetime.datetime.now()
            if today.weekday() != time[0] and today.weekday() < time[0]:
                days = (time[0] - today.weekday())
            elif today.weekday() != time[0] and today.weekday() > time[0]:
                days = (today.weekday() - time[0]) + 7
            elif today.weekday() == time[0] and today.hour > time[2][0]:
                days = 7
            elif today.weekday() == time[0] and today.hour < time[1][0]:
                days = 0
            next_raid = next_raid.replace(day=(today.day + days), hour=time[1][0], minute=time[1][1])
            raids.append(next_raid)
        raids.sort()
        return raids[0]

    @commands.command()
    async def raids(self):
        ''' Displays a list of all scheduled raid days '''
        raid_times = 'Current Raid Times:\n'
        for time in self.times:
            start_time = datetime.time(time[1][0], time[1][1])
            start_time = start_time.strftime('%-I:%M%p')
            end_time = datetime.time(time[2][0], time[2][1])
            end_time = end_time.strftime('%-I:%M%p')
            raid_times += '{} {} - {} (MST)\n'.format(self.days[time[0]], start_time, end_time)
        await self.bot.say('```{}```'.format(raid_times))

    @commands.command(pass_context=True)
    async def next(self, ctx):
        ''' Displays the next upcoming raid '''
        author = ctx.message.author
        today = datetime.datetime.now() - datetime.timedelta(hours=7)
        next_raid = self.find_next_raid(today)
        next_raid = relativedelta(next_raid, today)
        next_raid_str = '{} day(s), {} hour(s), {} mintue(s)'.format(str(next_raid.days), str(next_raid.hours), str(next_raid.minutes))
        await self.bot.say('<@!{}> The next raid is in {}'.format(author.id, next_raid_str))

    @commands.command(pass_context=True)
    async def guides(self, ctx):
        ''' Displays a list of available guides. Use !guides <search> for link to guide '''
        content = ctx.message.content.split()
        author = ctx.message.author
        with open('guides.json') as f:
            guides = json.load(f)
            if len(content) > 1:
                match = None
                for key in guides.keys():
                    if content[1].lower() in key.lower() and match == None:
                        match = key
                await self.bot.say(guides[match]['guide'])
            else:
                await self.bot.say('<@!{}> Available guides: {}'.format(author.id, ', '.join(guides.keys())))

    @commands.command(pass_context=True)
    async def videos(self, ctx):
        ''' Displays a list of available video guides. Use !videos <search> for link to video '''
        content = ctx.message.content.split()
        author = ctx.message.author
        with open('guides.json') as f:
            guides = json.load(f)
            if len(content) > 1:
                match = None
                for key in guides.keys():
                    if content[1].lower() in key.lower() and match == None:
                        match = key
                await self.bot.say(guides[match]['video'])
            else:
                await self.bot.say('<@!{}> Available video guides: {}'.format(author.id, ', '.join(guides.keys())))

    @commands.command(pass_context=True)
    async def logs(self, ctx):
        ''' Displays link to latest log recorded to warcraftlogs.com '''
        author = ctx.message.author
        logs = urllib.request.urlopen("https://www.warcraftlogs.com:443/v1/reports/user/garymjr?api_key={}".format(os.environ['WLOGS_API']))
        logs = json.loads(logs.read().decode('utf-8'))
        await self.bot.say('https://www.warcraftlogs.com/reports/{}'.format(logs[-1]['id']))

    @commands.command(pass_context=True)
    async def addons(self, ctx):
        ''' Displays a list of addons we use '''
        member = ctx.message.author
        ''' Displays a list of required raid addons '''
        with open('addons.json') as f:
            addons = json.load(f)
        reply = '\nRequired Addons:\n'
        for addon in addons['required']:
            reply += '\t{}: {}\n'.format(addon['name'], addon['url'])
        reply += 'Recommended Addons:\n'
        for addon in addons['recommended']:
            reply += '\t{}: {}\n'.format(addon['name'], addon['url'])
        await self.bot.say('{} Check your PM'.format(member.mention))
        await self.bot.send_message(member, reply)

    @commands.command()
    async def legionprep(self):
        ''' Displays Legion prep guide '''
        await self.bot.say('https://docs.google.com/spreadsheets/d/1hwvnNZEaSSj9YKui_2P9img-AN44TIoP-QsfA73qlGU/pubhtml#')

def setup(bot):
    bot.add_cog(Raids(bot))
