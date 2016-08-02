import datetime
import json
import math
import urllib.request
import os

import discord
import asyncio

def mention_user(user_id):
    return '<@!' + user_id + '>'

COMMANDS = [
    '!help',
    '!next',
    '!times',
    '!guides',
    '!videos',
    '!logs',
    '!code',
]

TIMES = [
    # day, start, end
    [3, [19, 0], [21, 0]],
    [5, [19, 0], [21, 0]],
]

DAYS = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

GUIDES = 'guides.json'

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as:', client.user.name, '-',  client.user.id)
    print('-----')

@client.event
async def on_message(message):
    content = message.content.split()
    print([message.author.id, message.channel.id, content])
    if content[0] == '!help':
        reply = ''
        for c in COMMANDS:
            reply += c + ', '
        await client.send_message(
            message.channel,
            mention_user(message.author.id) + ' Available commands: ' + reply[:-2])
    elif content[0] == '!next':
        today = datetime.datetime.now()
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
        next_raid = raids.pop(0)
        time = next_raid - today
        days = math.floor(time.total_seconds() / 86400)
        hours = math.floor((time.total_seconds() % 86400) / 3600)
        minutes = math.floor(((time.total_seconds() % 86400) % 3600) / 60)
        reply = str(days) + ' day(s), ' + str(hours) + ' hour(s), ' + str(minutes) + ' minute(s)'
        await client.send_message(
            message.channel,
            mention_user(message.author.id) + ' The next raid is in ' + reply)
    elif content[0] == '!times':
        reply = ''
        for raid in TIMES:
            date = datetime.time(raid[1][0], raid[1][1])
            reply += DAYS[raid[0]] + ' ' + date.strftime('%-I:%M%p - ')
            date = datetime.time(raid[2][0], raid[2][1])
            reply += date.strftime('%-I:%M%p (MST)') + '\n'
        await client.send_message(
            message.channel,
            'Current raid times:\n' + reply)
    elif content[0] == '!guides':
        file = open(GUIDES)
        keys = json.load(file)
        file.close()
        guides = []
        for key in keys:
            if keys[key]['guide'] != '':
                guides.append(key)
        reply = ''
        for guide in guides:
            reply += guide + ', '
        if len(content) > 1:
            for guide in guides:
                print([content[1], guide])
                if content[1].lower() in guide:
                    await client.send_message(message.channel, keys[guide]['guide'])
        else:
            await client.send_message(
                message.channel,
                mention_user(message.author.id) + ' Available guides: ' + reply[:-2])
    elif content[0] == '!videos':
        file = open(GUIDES)
        keys = json.load(file)
        file.close()
        videos = []
        for key in keys:
            if keys[key]['video'] != '':
                videos.append(key)
        reply = ''
        for video in videos:
            reply += video + ', '
        if len(content) > 1:
            for video in videos:
                if content[1].lower() in video:
                    await client.send_message(message.channel, keys[video]['video'])
        else:
            await client.send_message(
                message.channel,
                mention_user(message.author.id) + ' Available videos: ' + reply[:-2])
    elif content[0] == '!logs':
        logs = urllib.request.urlopen("https://www.warcraftlogs.com:443/v1/reports/user/garymjr?api_key=187bb410079c32b61d412a8838fb7542").read().decode('utf-8')
        logs = json.loads(logs)
        await client.send_message(
            message.channel,
            mention_user(message.author.id) + ' https://www.warcraftlogs.com/reports/' + logs[-1]['id'])
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

client.run(os.environ['DISCORD_API'])
