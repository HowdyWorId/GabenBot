from discord.ext import commands
from Bot.data import Data

class HelpCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command(name='help')
    async def help(self, ctx):
        await ctx.channel.send('lol')


def setup(bot):
    bot.add_cog(HelpCommands(bot))
