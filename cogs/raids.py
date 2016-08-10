from discord.ext import commands

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

	@commands.command()
	async def show_times(self):
		raid_times = 'Current Raid Times:\n'
		for time in self.times:
		    start_time = datetime.time(time[1][0], time[1][1])
		    start_time = start_time.strftime('%-I:%M%p')
		    end_time = datetime.time(time[2][0], time[2][1])
		    end_time = end_time.strftime('%-I:%M%p')
		    raid_times += '{} {} - {} (MST)\n'.format(self.days[time[0]], start_time, end_time)
		await self.bot.say('```{}```'.format(raid_times))

def setup(bot):
	bot.add_cog(Raids(bot))