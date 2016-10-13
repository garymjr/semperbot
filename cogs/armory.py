from discord.ext import commands

import discord
import urllib.request
import ast
import datetime
import os

class Armory:
    def __init__(self, bot):
        self.bot = bot

    def api(self, data):
        endpoint_url = 'https://us.api.battle.net/wow/{}/{}?fields={}&locale=en_US&apikey={}'.format(data['endpoint'], '/'.join(data['params']), ',+'.join(data['fields']), os.environ['BATTLENET_API'])
        try:
            results = urllib.request.urlopen(endpoint_url).read().decode('utf-8')
            results = ast.literal_eval(results)
        except urllib.error.HTTPError:
            results = None
        return results

    @commands.command(pass_context=True)
    async def ilvl(self, ctx):
        ''' Displays the ilvl of the specified character. Use !ilvl <character> '''
        content = ctx.message.content.split()
        if len(content) > 1:
            results = self.api({'endpoint':'character', 'params':['Dalaran', content[1]], 'fields':['items']})
            if results != None:
                ilvl = results['items']['averageItemLevel']
                await self.bot.say('{} has an item level of {}'.format(content[1], ilvl))

    @commands.command(pass_context=True)
    async def last(self, ctx):
        ''' Displays the last time the specified character was online. Use !last <character> '''
        content = ctx.message.content.split()
        if len(content) > 1:
            results = self.api({'endpoint':'character', 'params':['Dalaran', content[1]], 'fields':[]})
            if results != None:
                timestamp = results['lastModified']
                last_seen = datetime.datetime.fromtimestamp(int(timestamp) / 1e3) - datetime.timedelta(hours=7)
                await self.bot.say('{} was last seen online {} (MST)'.format(content[1], last_seen.strftime('%B %-d at %-I:%M%p')))


def setup(bot):
    bot.add_cog(Armory(bot))
