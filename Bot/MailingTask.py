import asyncio
from dataclasses import dataclass
from itertools import chain
from random import randint
from discord.ext import commands
from Bot.data.Data import Data
from Bot.extensions.VkParser import VkParser


@dataclass
class MailData:
    cached_posts = []


class MailingTask(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        asyncio.run(self.main())

    async def main(self):
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
            await self.mail(t, grs, channel) if not repeat else None

        r_post = posts[randint(0, len(posts) - 1)]

        if r_post not in MailData.cached_posts:
            # print(MailData.cached_posts)
            print(r_post)
            await self.send(r_post, channel)
            MailData.cached_posts.append(r_post)
            await asyncio.sleep(t)

        await self.mail(t, grs, channel) if not repeat else None

    async def send(self, post, channel_id):
        channel = self.bot.get_channel(channel_id)
        content = post['content']
        print(channel)
        # await channel.send(f"{content['text']} {content['attachments']}")


def setup(bot):
    bot.add_cog(MailingTask(bot))
