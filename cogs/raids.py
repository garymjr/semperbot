from discord.ext import commands
from dateutil.relativedelta import relativedelta

import discord
import datetime

class Raids:
	def __init__(self, bot):
		self.bot = bot
		self.times = [
			# day, start, end
			[3, [19, 0], [21, 0]],
			[5, [19, 0], [21, 0]],
		]

		self.days = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

	def find_next_raid(self, today):
	    raids = []
	    for time in self.times:
	        next_raid = datetime.datetime.now()
	        if today.weekday() != time[0] and today.weekday() < time[0]:
	            days = (time[0] - today.weekday())
	        elif today.weekday() != time[0] and today.weekday() > time[0]:
	            days = (today.weekday() - time[0]) + 7
	        elif today.weekday() == time[0] and today.hour > time[2][0]:
	            days = 7
	        elif today.weekday() == time[0] and today.hour < time[1][0]:
	            days = 0
	        next_raid = next_raid.replace(day=(today.day + days), hour=time[1][0], minute=time[1][1])
	        raids.append(next_raid)
	    raids.sort()
	    return raids[0]

	@commands.command()
	async def raids(self):
		''' Displays a list of all scheduled raid days '''
		raid_times = 'Current Raid Times:\n'
		for time in self.times:
		    start_time = datetime.time(time[1][0], time[1][1])
		    start_time = start_time.strftime('%-I:%M%p')
		    end_time = datetime.time(time[2][0], time[2][1])
		    end_time = end_time.strftime('%-I:%M%p')
		    raid_times += '{} {} - {} (MST)\n'.format(self.days[time[0]], start_time, end_time)
		await self.bot.say('```{}```'.format(raid_times))

	@commands.command(pass_context=True)
	async def next(self, ctx):
		''' Displays the next upcoming raid '''
		today = datetime.datetime.now() - datetime.timedelta(hours=7)
		next_raid = self.find_next_raid(today)
		next_raid = relativedelta(next_raid, today)
		next_raid_str = '{} day(s), {} hour(s), {} mintue(s)'.format(str(next_raid.days), str(next_raid.hours), str(next_raid.minutes))
		await self.bot.say('<@!{}> The next raid is in {}'.format(ctx.message.author.id, next_raid_str))

def setup(bot):
	bot.add_cog(Raids(bot))