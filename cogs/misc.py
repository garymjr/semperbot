from discord.ext import commands
from datetime import datetime

import discord
import urllib.request
import ast
import json

class Misc:
	def __init__(self, bot):
		self.bot = bot

	def format_timedelta(duration):
		days = duration // 86400
		hours = (duration % 86400) // 3600
		minutes = ((duration % 86400) % 3600) // 60
		seconds = (((duration % 86400) % 3600) % 60)
		if days > 0:
			time_string = '{} days, {} hours, {} minutes, {} seconds'.format(days, hours, minutes, seconds)
		elif hours > 0:
			time_string = '{} hours, {} minutes, {} seconds'.format(hours, minutes, seconds)
		elif minutes > 0:
			time_string = '{} minutes, {} seconds'.format(days, hours, minutes, seconds)
		else:
			time_string = '{} seconds'.format(seconds)
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

	@commands.command(hidden=True)
	async def ping(self):
		''' Pings the bot to see if it's alive and returns uptime '''
		now = datetime.now()
		duration = (now - self.bot.uptime).total_seconds()
		await self.bot.say("Pong! I've been alive for {}".format(self.format_timedelta(duration)))

def setup(bot):
	bot.add_cog(Misc(bot))