# Python 3.7.3
# https://discordapp.com/oauth2/authorize?&client_id=702107949421822104&scope=bot&permissions=2147483639
import logging
import os
import random

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

token = os.environ.get('BOT_TOKEN')
bot.run(token)

