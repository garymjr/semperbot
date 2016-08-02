import datetime
import json
import math
import urllib.request
import os
import ast

import discord
import asyncio

from dateutil.relativedelta import relativedelta

def mention_user(user_id):
    return '<@!' + user_id + '>'

COMMANDS = [
    '!help',
    '!next',
    '!times',
    '!guides',
    '!videos',
    '!logs',
    '!wiki'
    '!code',
]

TIMES = [
    # day, start, end
    [3, [19, 0], [21, 0]],
    [5, [19, 0], [21, 0]],
]

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as:', client.user.name, '-',  client.user.id)
    print('-----')

@client.event
async def on_message(message):
    content = message.content.split()
    print([message.author.id, message.channel.id, content])
    reply = ''
    if content[0] == '!help':
        await client.send_message(
            message.channel,
            mention_user(message.author.id) + ' Available commands: ' + ', '.join(COMMANDS))
    elif content[0] == '!next':
        today = datetime.datetime.now() - datetime.timedelta(hours=7)
        next_raid = find_next_raid(today)
        reply = next_raid_string(today, next_raid)
        await client.send_message(
            message.channel,
            mention_user(message.author.id) + ' The next raid is in ' + reply)
    elif content[0] == '!times':
        for raid in TIMES:
            date = datetime.time(raid[1][0], raid[1][1])
            reply += date.strftime('%A %-I:%M%p - ')
            date = datetime.time(raid[2][0], raid[2][1])
            reply += date.strftime('%-I:%M%p (MST)') + '\n'
        await client.send_message(
            message.channel,
            'Current raid times:\n' + reply)
    elif content[0] in ['!guides', '!videos']:
        user_request = content[0][1:-1]
        file = open('guides.json')
        keys = json.load(file)
        file.close()
        if len(content) > 1:
            for key in keys:
                if content[1].lower() in key:
                    await client.send_message(message.channel, keys[key][user_request])
        else:
            await client.send_message(
                message.channel,
                mention_user(message.author.id) + ' Available ' + content[0][1:] + ': ' + ', '.join(keys))
    elif content[0] == '!logs':
        logs = urllib.request.urlopen("https://www.warcraftlogs.com:443/v1/reports/user/garymjr?api_key=187bb410079c32b61d412a8838fb7542").read().decode('utf-8')
        logs = json.loads(logs)
        await client.send_message(
            message.channel,
            mention_user(message.author.id) + ' https://www.warcraftlogs.com/reports/' + logs[-1]['id'])
    elif content[0] == '!wiki':
        if len(content) > 1:
            results = urllib.request.urlopen("https://en.wikipedia.org/w/api.php?action=opensearch&search=" + '%20'.join(content[1:])).read().decode('utf-8')
            results = ast.literal_eval(results)
            if len(results[3]) > 0:
                await client.send_message(
                    message.channel,
                    mention_user(message.author.id) + ' ' + results[3][0])
            else:
                await client.send_message(
                    message.channel,
                    mention_user(message.author.id) + " I wasn't able to find any results")
    elif content[0] == '!code':
        await client.send_message(
            message.channel,
            mention_user(message.author.id) + ' https://github.com/garymjr/semperbot')
    elif content[0] == '!poe':
        await client.send_message(
            message.channel,
            mention_user('125071902556291072') + ' tap tap tap')
    elif content[0] == '!hunters':
        await client.send_message(
            message.channel,
            mention_user('207175112691023872') + ' I heard you love hunters!')
    elif content[0] == '!tacos':
        await client.send_message(
            message.channel,
            mention_user(message.author.id) + ' https://www.google.com/maps/search/tacos/')

def next_raid_string(now, next):
    next_raid = relativedelta(next, now)
    return "{} day(s), {} hour(s), {} mintue(s)".format(str(next_raid.days), str(next_raid.hours), str(next_raid.minutes))

def find_next_raid(today):
    raids = []
    for raid in TIMES:
        next_raid = datetime.datetime.now()
        if today.weekday() != raid[0] and today.weekday() < raid[0]:
            days = (raid[0] - today.weekday())
        elif today.weekday() != raid[0] and today.weekday() > raid[0]:
            days = (today.weekday() - raid[0]) + 7
        elif today.weekday() == raid[0] and today.hour > raid[2][0]:
            days = 7
        elif today.weekday() == raid[0] and today.hour < raid[1][0]:
            days = 0
        next_raid = next_raid.replace(day=(today.day + days), hour=raid[1][0], minute=raid[1][1])
        raids.append(next_raid)
    raids.sort()
    return(raids[0])

client.run(os.environ['DISCORD_API'])
