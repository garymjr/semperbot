from discord.ext import commands
from datetime import datetime
from dateutil.relativedelta import relativedelta

import discord
import urllib.request
import ast
import json
import math

class Misc:
	def __init__(self, bot):
		self.bot = bot

	def format_time(self, uptime):
		if uptime.days > 0:
			time_string = '{} days, {} hours, {} minutes, {} seconds'.format(uptime.days, uptime.hours, uptime.minutes, uptime.seconds)
		elif uptime.hours > 0:
			time_string = '{} hours, {} minutes, {} seconds'.format(uptime.hours, uptime.minutes, uptime.seconds)
		elif uptime.minutes > 0:
			time_string = '{} minutes, {} seconds'.format(uptime.minutes, uptime.seconds)
		else:
			time_string = '{} seconds'.format(uptime.seconds)
		return time_string


	@commands.command(pass_context=True)
	async def wiki(self, ctx):
		''' Displays search results from wowpedia. Use !wiki <search> '''
		content = ctx.message.content.split()
		if len(content) > 1:
			req = urllib.request.Request('http://wow.gamepedia.com/api.php?action=opensearch&search={}'.format('%20'.join(content[1:])), headers={'User-Agent': 'Mozilla/5.0'})
			results = urllib.request.urlopen(req).read().decode('utf-8')
			results = ast.literal_eval(results)
			await self.bot.say(results[3][0])

	@commands.command(pass_context=True)
	async def discord(self, ctx):
		''' Displays known discord class channels. Use !discord <class> for channel invite '''
		content = ctx.message.content.split()
		author = ctx.message.author
		with open('channels.json') as f:
			channels = json.load(f)
			if len(content) > 1:
				match = None
				for key in channels.keys():
					if content[1] in key and match == None:
						match = key
				await self.bot.say(channels[match])
			else:
				await self.bot.say('<@!{}> Known discord class channels: {}'.format(author.id, ', '.join(channels.keys())))

	@commands.command()
	async def code(self):
		''' Displays bot github page '''
		await self.bot.say('https://github.com/garymjr/semperbot')

	@commands.command()
	async def ping(self):
		''' Pings the bot to see if it's alive and returns uptime '''
		now = datetime.now()
		uptime = relativedelta(now, self.bot.uptime)
		await self.bot.say("Pong! I've been alive for {}".format(self.format_time(uptime)))

	@commands.command(hidden=True)
	async def creed(self):
		txt = '```'
		txt += 'Raiders Creed:\n'
		txt += 'A) You put forth effort to be the best at your class you can be.\n\n'
		txt += 'B) You want to conquer all the end-game raid content Legion offers.\n\n'
		txt += 'C) You learn from your mistakes. You are able to take criticism, and grow from it.\n\n'
		txt += 'D) You come prepared, Bringing your own potions/flasks, and you read up on fights\nas needed. You are on time to the raids and you never make excuses. You take personal\nresponsibility for your own performance, never blame others for your own faults.  If you have a problem with a\nfellow raider you\ntake it up with an officer or higher up.'
		txt += '```'
		await self.bot.say(txt)

def setup(bot):
	bot.add_cog(Misc(bot))