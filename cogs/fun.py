from discord.ext import commands

import discord

class Fun:
	def __init__(self, bot):
		self.bot = bot

	@commands.command(hidden=True)
	async def poe(self):
		await self.bot.say('<@!125071902556291072> tap tap tap')

	@commands.command(hidden=True)
	async def hunters(self):
		await self.bot.say('<@!207175112691023872> I heard you love hunters!')

	@commands.command(hidden=True)
	async def tacos(self):
		await self.bot.say('https://www.google.com/maps/search/tacos/')

def setup(bot):
	bot.add_cog(Fun(bot))