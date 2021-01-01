import asyncio
from Bot.cogs.BackgroundEvents import BackgroundEvents as be
import discord
from discord.ext import commands

from Bot.data import Data


class Administrator(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.role_muted = 'Muted'  # later, u need to add roles names to Data class
        self.data = Data.Data()
        self.muted_members = []

    @commands.command(name='mute')
    async def mute(self, member: discord.member.Member, time: int, *, reason):
        role = discord.utils.get(member.guild.roles, name=self.role_muted)
        await member.add_roles(role)
        print(f'{member} has been muted for {time} with reason {reason}')
        await asyncio.sleep(10)
        await member.remove_roles(role)

    @commands.command(name='clear')
    async def clear(self, ctx, amount=1):
        channel = ctx.channel
        member = ctx.author
        if member.id in self.data.head_admins:
            await channel.purge(limit=amount + 1)

    @commands.command(name='meme')
    async def meme(self, ctx):
        vk_mail = self.data.vk_mail
        await ctx.message.delete()
        if 'meme' in vk_mail:
            meme = vk_mail['meme']
            # print(*meme.values(), False)
            await be(self.bot).to_mail('meme')
        # print('lol')

    @commands.command(name='add_vk_mailing')
    async def add_vk_mailing(self, ctx, name_app, group_id, channel_id=None):
        await ctx.channel.send(f'{name_app}, {group_id}, {channel_id}')

    @commands.command(name='send')
    @commands.has_any_role('Admin', 'Holmes', 'Watson')
    async def send(self, ctx, channel_id: int, *, message: str):
        channel = self.bot.get_channel(channel_id)
        await channel.send(message)
        await ctx.message.delete()

    @commands.command(name='mute_us')
    @commands.has_role('Admin')
    async def mute_us(self, ctx, bool=True):
        await ctx.message.delete()
        member = ctx.message.author
        voice = member.voice

        if not hasattr(voice, 'channel'):
            await member.send('v kanal zaidi')
            return ''

        channel = voice.channel
        voice_channel = discord.utils.get(ctx.message.guild.channels, name=f"{channel}",
                                          type=discord.ChannelType.voice)
        guild = ctx.message.guild
        member_ids = list(voice_channel.voice_states.keys())
        members = [await guild.fetch_member(m_id) for m_id in member_ids]

        for member in members:
            self.muted_members.append(member)
            await member.edit(mute=bool)

    @commands.command(name='unmute_us')
    @commands.has_role('Admin')
    async def unmute_us(self, ctx):
        await ctx.message.delete()
        for member in self.muted_members:
            await member.edit(mute=False)
        self.muted_members.clear()

    @commands.command(name='get_info')
    @commands.has_role('Admin')
    async def get_info_from_voice(self, ctx, channel_id):
        await self.bot.wait_until_ready()
        channel = ctx.message.author.voice.channel
        voice_channel = discord.utils.get(ctx.message.guild.channels, name=f"{channel}",
                                          type=discord.ChannelType.voice)
        member_ids = voice_channel.voice_states.keys()
        print(member_ids)
        # return channel.members


def setup(bot):
    bot.add_cog(Administrator(bot))
