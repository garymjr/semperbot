from discord.ext import commands
from dateutil.relativedelta import relativedelta
from collections import Counter

import discord
import datetime
import asyncio
import copy
import os

initial_extensions = [
	'cogs.raids',
]

prefix = ['!']
bot = commands.Bot(command_prefix=prefix, description='SemperBot', pm_help=None)

@bot.event
async def on_ready():
	print('Logged in as:')
	print('Username: {}'.format(bot.user.name))
	print('ID: {}'.format(bot.user.id))
	print('----------')

@bot.event
async def on_command(command, ctx):
	bot.commands_used[command.name] += 1
	print(bot.commands_used)

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