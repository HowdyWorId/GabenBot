import asyncio
from dataclasses import dataclass
from itertools import chain
from random import randint
from discord.ext import commands, tasks
from Bot.data.Data import Data
from Bot.extensions.VkParser import VkParser


@dataclass
class MailData:
    cached_posts = []


class BackgroundEvents(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        # self.mailing_main.start()

    @tasks.loop(hours=100000)
    async def mailing_main(self):
        await self.bot.wait_until_ready()
        tasks = [asyncio.create_task(self.mail(v['time'],
                                               v['group_ids'],
                                               v['channel_id'])) for k, v in Data.vk_mail.items()]

        for t in tasks:
            await t

    async def mail(self, t, grs, channel, repeat=True):
        posts = list(chain(*[VkParser().get_posts(l) for
                             l in grs]))
        posts = [el for el in posts if el not in MailData.cached_posts]
        if len(posts) == 0:
            await asyncio.sleep(t)
            await self.mail(t, grs, channel) if repeat else None

        r_post = posts[randint(0, len(posts) - 1)]

        if r_post not in MailData.cached_posts:
            await self.send(r_post, channel)
            MailData.cached_posts.append(r_post)
            await asyncio.sleep(t)

        await self.mail(t, grs, channel) if repeat else None

    async def to_mail(self, name: str):
        if name in Data.vk_mail:
            await self.mail(*Data.vk_mail[name], False)

    async def send(self, post, channel_id: int):
        channel = self.bot.get_channel(channel_id)
        content = post['content']
        await channel.send(f"{content['text']}") if content['text'] is not '' else None
        for a in content['attachments']:
            await channel.send(f"{a}")


def setup(bot):
    bot.add_cog(BackgroundEvents(bot))
