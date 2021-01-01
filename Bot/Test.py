import asyncio
from dataclasses import dataclass
from itertools import chain
from random import randint

from Bot.data.Data import Data
from Bot.extensions.VkParser import VkParser


@dataclass
class MailData:
    cached_posts = []


async def mail(t, grs, channel, repeat=True):
    posts = list(chain(*[VkParser().get_posts(l) for
                         l in grs]))
    posts = [el for el in posts if el not in MailData.cached_posts]
    if len(posts) == 0:
        await asyncio.sleep(t)
        await mail(t, grs, channel) if not repeat else None

    r_post = posts[randint(0, len(posts) - 1)]

    if r_post not in MailData.cached_posts:
        print(MailData.cached_posts)
        print(r_post)
        MailData.cached_posts.append(r_post)
        await asyncio.sleep(t)

    await mail(t, grs, channel) if not repeat else None


async def main():
    tasks = [asyncio.create_task(mail(v['time'],
                                      v['group_ids'],
                                      v['channel_id'])) for k, v in Data.vk_mail.items()]

    for t in tasks:
        await t


if __name__ == '__main__':
    asyncio.run(main())
