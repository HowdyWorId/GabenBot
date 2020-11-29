import os
import random
import asyncio
import requests, re
from bs4 import BeautifulSoup, SoupStrainer
import discord
from discord.ext import commands

osk = ['иди нахуй']
ban_prefix = ['-', '#', ['!zt']]
protect_channel = ['общение', 'meme', 'ссылки', 'получение-ролей']
black_list = ['TeeSey#5157', 'Groovy#7254', 'ProBot ✨#5803', ]
admins = ['TheBeST#5143', 'C.O.D.E.X#5794', ]
muted_members = []
used_memes = []
pubs_ = ['https://vk.com/oryslenti', 'https://vk.com/public171746659',
        'https://vk.com/nestandartniememi', 'https://vk.com/chlgpro',
        'https://vk.com/shkolkrim']

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')
TOKEN = os.environ.get('BOT_TOKEN')

def check_admin(msg):
    try:
        if str(msg.author) in admins:
            return True
        return False
    except Exception as error:
        print(error)
        if str(msg.message.author) in admins:
            return True
        return False

class Meme:
    def __init__(self, urls, info=False):
        self.__urls = urls
        self.__problem_publics = []
        self.__memes = self.meme_generator()

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
                        meme_url = rel[0][1:-1]
                        if 'jpg?' not in meme_url:
                            d.append({'public': url, 'meme': ['', meme_url]})
                        else:
                            # print('raising Exception')
                            raise Exception

            except Exception:
                # print(f"can't parse to  {url}")
                self.__problem_publics.append(url)
                continue
        return d

    @property
    def problem_publics(self):
        return list(set(self.__problem_publics))

    @property
    def current_publics(self):
        return self.__urls

    @property
    def memes(self):
        return self.__memes


pubs_ = {'https://vk.com/oryslenti', 'https://vk.com/public171746659',
        'https://vk.com/nestandartniememi', 'https://vk.com/chlgpro',
        'https://vk.com/shkolkrim'}


async def background_task(bool=True):
    await bot.wait_until_ready()
    m = Meme(pubs_).memes
    channel = bot.get_channel(764760007681900574)
    # channel = bot.get_channel(761600162501754910)
    if bot.is_closed:
        r = random.randint(0, len(m) - 1)
        memes = [m[r]['meme']]
        for meme in memes:
            await channel.send(f'{meme[0]}\n {"".join(meme[1])}')
        await asyncio.sleep(random.randint(1000, 40000))
        if bool:
            await background_task()
    else:
        print('bot is closed')


async def mute_members(member, time=120, reason=''):
    if member.author not in muted_members:
        role = discord.utils.get(member.guild.roles, name='Muted')
        muted_members.append(member.author)
        index = muted_members.index(member.author)
        await member.author.add_roles(role)
        await member.author.send('Отдохни дружок, чаяку выпей.Тебя замутили на %s сек :)' % time)
        await asyncio.sleep(time)
        print(f'Прошло {time}')
        await member.author.remove_roles(role)
        muted_members.pop(index)

@bot.event
async def on_ready():
    game = discord.Game("Robbery of Schoolchildren")
    await bot.change_presence(status=discord.Status.idle, activity=game, afk=True)
    print('Bot logged as {}'.format(bot.user))


@bot.event
async def on_member_join(member):
    phrases = ['У нас новый чел {0.mention}.', 'К нам присоединился, {0.mention}', 'Приветствуем тебя, {0.mention}', ]
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
    # AntiSPAM
    messages = list(bot.cached_messages)
    if not message.author.bot and message.author not in muted_members:
        if len(messages) > 5:

            messages_from_5_times = [(messages[-i].created_at - messages[-5].created_at).seconds for i in range(1, 5)]
            messages_from_5_author = [(messages[-i].author == messages[-5].author) for i in range(1, 5)]

            if sum(messages_from_5_times) < 5 and all(messages_from_5_author):
                print('spamming')
                await message.channel.purge(limit=5)
                await message.channel.send('{0.author.mention} STOP SPAMMING!!!'.format(message)) if message.author not in muted_members else None
                await mute_members(message, random.randint(100,300))

            elif all([messages[-i].content == messages[-1].content for i in range(1,5)]):
                print('spam 4 duplicates')
                await message.channel.purge(limit=4)
                await mute_members(message, random.randint(100,300))


@bot.command(pass_context=True)
async def clear(ctx, amount=10):
    if check_admin(ctx):
        print(f'INFO:{ctx.message.author} delete {amount + 1} messages.')
        await ctx.channel.purge(limit=amount + 1)
    else:
        await ctx.channel.send('{0.author.mention} Иди нах :)'.format(ctx.message))


@bot.command(pass_context=False)
async def meme(ctx):
    if check_admin(ctx):
        await ctx.message.delete()
        await background_task(False)


@bot.command(pass_context=False)
async def problem_pubs(ctx):
    if check_admin(ctx):
        channel = bot.get_channel(761600162501754910)
        await channel.send(Meme(urls=pubs_).problem_publics)

@bot.command(pass_context=False)
async def pubs(ctx):
    if check_admin(ctx):
        channel = bot.get_channel(761600162501754910)
        await channel.send('```%s```' % '\n'.join(pubs_))

with open('requirements.txt', 'r') as f:
                               print(f.read())
f.close()
meme_task = bot.loop.create_task(background_task())
bot.run(os.environ.get('BOT_TOKEN'))
