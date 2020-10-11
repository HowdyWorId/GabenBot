import logging
import os
import random
import asyncio
import requests, re
from bs4 import BeautifulSoup, SoupStrainer

logging.basicConfig(filename="logs.log", level=logging.INFO, filemode='w')
log_message = logging.getLogger('messsage')
osk = ['даун', 'бот даун', 'ты даун', 'довн']
ban_prefix = ['-', '#', ['!zt']]
protect_channel = ['общение', 'meme', 'ссылки', 'получение-ролей']
black_list = ['TeeSey#5157', 'Groovy#7254', 'ProBot ✨#5803', ]
admins = ['TheBeST#5143', 'C.O.D.E.X#5794', ]

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

class Meme:
    def __init__(self, urls=['https://vk.com/oryslenti', 'https://vk.com/public171746659',
        'https://vk.com/nestandartniememi', 'https://vk.com/chlgpro',
        'https://vk.com/shkolkrim']):
        self.__urls = urls
        self.__memes = self.meme_generator()
        # print(self.__memes)


    def meme_generator(self):
        d = []
        for url in self.__urls:
            r = requests.get(url)
            soup = BeautifulSoup(r.content, 'html.parser',
                                 parse_only=SoupStrainer('div'))

            convert = soup.find_all('div', {'class': "wi_body wi_no_text"})
            try:
                for el in convert[1:]:
                    rel = re.findall(r'url(.*?);', str(el))
                    if len(rel) == 1:
                        d.append({'public':url, 'meme':['',rel[0][1:-1]],})
            except Exception:
                print(f'cant parse to {url}')
                continue
        return d

    @property
    def publics(self):
        return self.__urls

    @property
    def memes(self):
        return self.__memes

    @staticmethod
    def new_urls(urls):
        return Meme(urls=urls)


async def background_task():
    m = Meme().memes
    await bot.wait_until_ready()
    channel = bot.get_channel(701437053593714720)
    # channel = bot.get_channel(761600162501754910)
    if bot.is_closed:
        r = random.randint(0,len(m)-1)
        memes = [m[r]['meme']]
        print(memes)
        for meme in memes:
            await channel.send(f'{meme[0]}\n {"".join(meme[1])}')
        await asyncio.sleep(random.randint(1000,40000))
        await background_task()
    else:
        print('bot is closed')



@bot.event
async def on_ready():
    game = discord.Game("Robbery of Schoolchildren")
    await bot.change_presence(status=discord.Status.idle, activity=game, afk=True)
    print('Bot logged as {}'.format(bot.user))


@bot.event
async def on_member_join(member):
    phrases = ['У нас новый чел {0.mention}.', 'К нам присоединился {0.mention}', 'Приветствуем тебя, {0.mention}', ]
    channel = bot.get_channel(660210563342794824)
    r = random.randint(0, len(phrases) - 1)
    await channel.send(str(phrases[r]).format(member))


@bot.event
async def on_message(message):
    print(f'INFO:{message.author} send "{message.content}" to channel "{message.channel}"')
    msg = message.content.lower()
    if str(message.author) not in black_list:
        await bot.process_commands(message)

        if msg in osk:
            await message.channel.send('я твое очко наизнку вертел')

    else:
        if str(message.author) != 'Groovy#7254' and str(message.author) != 'ProBot ✨#5803':
            print(f'WARNING:{message.author} send "{message.content}" to channel {message.channel}')

    try:
        if str(msg)[0] in ban_prefix and str(message.channel).lower() in protect_channel:
            await message.channel.purge(limit=1)
    except IndexError:
        if str(message.author) == 'Groovy#7254' or str(message.author) == 'ProBot ✨#5803':
            if str(message.channel).lower() in protect_channel:
                print(f'INFO:delete "{message.content}" in channel "{message.channel}"')
                await message.channel.purge(limit=1)


@bot.command(pass_context=True)
async def clear(ctx, amount=10):
    if str(ctx.message.author) in admins:
        print(f'INFO:{ctx.message.author} delete {amount + 1} messages.')
        await ctx.channel.purge(limit=amount + 1)
    else:
        await ctx.channel.send('{0.author.mention} Иди нах :)'.format(ctx.message))


meme_task = bot.loop.create_task(background_task())
token = os.environ.get('BOT_TOKEN')
bot.run(token)
