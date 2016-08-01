from datetime import datetime
import json

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
    '!code',
]

TIMES = [
    [3, 'thursday', [19, 0], [21, 0]],
    [5, 'saturday', [19, 0], [21, 0]],
]

GUIDES = open('guides.json')

class SemperBot(discord.Client):

    @asyncio.coroutine
    def on_ready(self):
        print('Logged in as:', self.user.name, '-',  self.user.id)
        print('-----')

    @asyncio.coroutine
    def on_message(self, message):
        content = message.content.split()
        print([message.author.id, message.channel.id, content])
        if content[0] == '!help':
            reply = ''
            for c in COMMANDS:
                reply += c + ', '
            yield from self.send_message(
                message.channel,
                mention_user(message.author.id) + ' Available commands: ' + reply[:-2])
        elif content[0] == '!next':
            pass
        elif content[0] == '!times':
            pass
        elif content[0] == '!guides':
            keys = json.load(GUIDES)
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
                        yield from self.send_message(message.channel, keys[guide]['guide'])
            else:
                yield from self.send_message(
                    message.channel,
                    mention_user(message.author.id) + ' Available guides: ' + reply[:-2])
        elif content[0] == '!videos':
            keys = json.load(GUIDES)
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
                        yield from self.send_message(message.channel, keys[video]['video'])
            else:
                yield from self.send_message(
                    message.channel,
                    mention_user(message.author.id) + ' Available videos: ' + reply[:-2])
        elif content[0] == '!code':
            yield from self.send_message(
                message.channel,
                mention_user(message.author.id) + ' https://github.com/garymjr/semperbot')
        elif content[0] == '!poe':
            yield from self.send_message(
                message.channel,
                mention_user('125071902556291072') + ' tap tap tap')
        elif content[0] == '!hunters':
            yield from self.send_message(
                message.channel,
                mention_user('207175112691023872') + ' I heard you love hunters!')

client = SemperBot()
client.run('***REMOVED***')