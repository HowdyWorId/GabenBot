# Python 3.7.3
# https://discordapp.com/oauth2/authorize?&client_id=702107949421822104&scope=bot&permissions=2147483639
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
black_list = ['напердел#5157', 'Groovy#7254', 'ProBot ✨#5803', ]
admins = ['TheBeST#5143', 'C.O.D.E.X#5794', ]

import discord
from discord.ext import commands

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

async def background_task():
    urls = ['https://vk.com/oryslenti','https://vk.com/public171746659', 'https://vk.com/fails66','https://vk.com/nestandartniememi','https://vk.com/willscary','https://vk.com/chlgpro','https://vk.com/shkolkrim']
    def meme_generator(urls: list = urls):
        lst = []
        for url in urls:
            r = requests.get(url)  # /photo-171746659_457350338?list=wall-171746659_1801160&amp
            soup = BeautifulSoup(r.content, 'html.parser',
                                 parse_only=SoupStrainer('div'))  # ,parse_only=SoupStrainer('a')
            # print(soup)

            try:
                convert = soup.find_all('div', {'class': "wi_body wi_no_text"})
                if convert == []:
                    print(f'cant parse to {url}')
                    raise IndexError
                for el in convert:
                    jpg = [i[1:-1] for i in re.findall(r'url(.*?);', str(el))]
                    lst.append(['', jpg])

            except IndexError:
                convert = soup.find_all('div', {'class': 'wi_body'})
                for el in convert:
                    jpg = [i[1:-1] for i in re.findall(r'url(.*?);', str(el))]
                    text = re.findall(r'<div class="pi_text">(.*?)</div>', str(el))[0]
                    if len(jpg) < 2:
                        lst.append([text, jpg])

        return lst

    await bot.wait_until_ready()
    channel = bot.get_channel(701437053593714720)
    if bot.is_closed:
        memes = meme_generator()
        memes = [ memes[random.randint(0,len(memes)-1)] for _ in range(0,5) ]
        # memes = list(set(memes))
        # print(memes)
        for meme in memes:
            await channel.send(f'{meme[0]}\n {" ".join(meme[1])}')
        await asyncio.sleep(36000)
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


bot.loop.create_task(background_task())
token = os.environ.get('BOT_TOKEN')
bot.run(token)
