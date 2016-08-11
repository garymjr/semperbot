from discord.ext import commands

import discord
import urllib.request
import ast
import json

class Misc:
	def __init__(self, bot):
		self.bot = bot

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

def setup(bot):
	bot.add_cog(Misc(bot))