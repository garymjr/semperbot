from discord.ext import commands
from cogs.utils import config

import discord

class Admin:
	def __init__(self, bot):
		self.bot = bot
		self.config = config.Config('config.json')

	@commands.group(hidden=True, pass_context=True)
	async def admin(self, ctx):
		author = ctx.message.author
		mods = self.config.get('mods') if self.config.get('mods') else []
		if not author.id == '214442677523972098' and author.id in mods:
			await self.bot.say('{} Sorry, command not allowed!'.format(author.mention))

	@admin.command(pass_context=True)
	async def mod(self, ctx):
		author = ctx.message.author
		content = ctx.message.content.split()
		mods = self.config.get('mods') if self.config.get('mods') else []
		if content[2] == 'add':
			mods.append(content[3])
			self.config.set('mods', mods)
			await self.bot.say('Added <@!{}> to mod group'.format(content[3]))
		elif content[2] == 'rem':
			mods.remove(content[3])
			self.config.set('mods', mods)
			await self.bot.say('Removed <@!{}> from mod group'.format(content[3]))
		elif content[2] == 'list':
			mods_list = []
			for mod in mods:
				mods_list.append('<@!{}>'.format(mod))
			await self.bot.say('Current mods: {}'.format(', '.join(mods_list)))

def setup(bot):
	bot.add_cog(Admin(bot))