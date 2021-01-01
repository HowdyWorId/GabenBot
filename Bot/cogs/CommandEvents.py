from random import randint

import discord

from Bot.data import Data
from discord.ext import commands
from Bot.cogs import Administrator as Admin


class CommandEvents(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.data = Data.Data()
        self.msgs_count = 0

    @commands.Cog.listener()
    async def on_message(self, msg):
        self.msgs_count += 1
        member = msg.author
        channel = msg.channel
        if member.bot:
            if member != self.bot.user:
                # Protection from Music bots
                if channel not in self.data.channels['unprotect_channels']:
                    if str(member) in ['Groovy#7254', 'ProBot ✨#5803']:
                        await msg.channel.purge(limit=2)
                    else:
                        await msg.delete()
        else:
            # ANTISPAM
            if len(list(self.bot.cached_messages)) >= 4:
                msgs = list(self.bot.cached_messages)[-4:]
                if sum([(msgs[-i].created_at - msgs[-4].created_at).seconds for i in range(1, 4)]) <= 3 and all(
                        [(msgs[-i].author == msgs[-4].author) for i in range(1, 4)]):
                    a = Admin.Administrator(self.bot)
                    await a.mute(a, member=member, time=20, reason='ANTISPAM_sys')

    @commands.Cog.listener()
    async def on_member_join(self, member):
        channel = member.guild.system_channel
        if channel is not None:
            greetings = self.data.messages["greetings"]
            await channel.send(greetings[randint(0, len(greetings))].format(member.author))

    @commands.Cog.listener()
    async def on_ready(self):
        print('Bot {} is online!'.format(self.bot.user))
        game = discord.Game("твою жизнь")
        await self.bot.change_presence(status=discord.Status.idle, activity=game)


def setup(bot):
    bot.add_cog(CommandEvents(bot))
