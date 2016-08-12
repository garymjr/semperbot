from discord.ext import commands
from collections import Counter

import discord
import asyncio
import os
import json

initial_extensions = [
	'cogs.raids',
	'cogs.misc',
	'cogs.armory',
	'cogs.fun',
]

description = '''
A discord bot for Semper Para Bellum
'''

prefix = ['!']
bot = commands.Bot(command_prefix=prefix, description=description, pm_help=None)

@bot.event
async def on_ready():
	print('Logged in as:')
	print('Username: {}'.format(bot.user.name))
	print('ID: {}'.format(bot.user.id))
	print('----------')

@bot.event
async def on_command(command, ctx):
	bot.commands_used[command.name] += 1

@bot.event
async def on_message(message):
	if message.author.bot:
		return

	await bot.process_commands(message)

if __name__ == '__main__':
	bot.commands_used = Counter()
	for ext in initial_extensions:
		try:
			bot.load_extension(ext)
		except Exception as e:
			print('Failed to load extension {}\n{}: {}'.format(ext, type(e).__name__, e))
	bot.run(os.environ['DISCORD_API'])