from discord.ext import commands
from cogs.utils import config

import discord

class Fun:
    def __init__(self, bot):
        self.bot = bot

    @commands.command(hidden=True)
    async def poe(self):
        await self.bot.say('<@!125071902556291072> tap tap tap')

    @commands.command(hidden=True)
    async def aj(self):
        await self.bot.say("<@!207175112691023872> Hey where'd you get those desks?")

    @commands.command(hidden=True)
    async def no(self):
        await self.bot.say("<@!125071902556291072> You're wrong.")

    @commands.command(hidden=True)
    async def hunters(self):
        await self.bot.say('<@!207175112691023872> I heard you love hunters!')

    @commands.command(hidden=True)
    async def tacos(self):
        await self.bot.say('https://www.google.com/maps/search/tacos/')

    @commands.command(hidden=True, pass_context=True)
    async def stats(self, ctx):
        author = ctx.message.author
        stats = self.bot.stats.get(author.id)
        if stats:
            await self.bot.say('```Message Count: {}\tWord Count: {}\tPoints: {}```'.format(stats['count'], stats['words'], stats['points']))

def setup(bot):
    bot.add_cog(Fun(bot))
