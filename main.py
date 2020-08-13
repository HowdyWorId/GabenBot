# Python 3.7
# https://discordapp.com/oauth2/authorize?&client_id=702107949421822104&scope=bot&permissions=2147483639
import logging
logging.basicConfig(filename="logs.log", level=logging.INFO,filemode='w')
log_message = logging.getLogger('messsage')
dawn = ['даун','бот даун', 'ты даун', 'довн']
ban_prefix = ['-', '#', ['!zt']]
protect_channel = ['общение','meme','ссылки','получение-ролей']
black_list = ['напердел#5157', 'Groovy#7254','ProBot ✨#5803',]
admins = ['TheBeST#5143', 'C.O.D.E.X#5794',]

import discord
from discord.ext import commands

token = 'NzAyMTA3OTQ5NDIxODIyMTA0.Xp7O-w.nrbKw_c3PT5JcVFhSAxiTvCS1Vw'
client_id = 702107949421822104

bot = commands.Bot(command_prefix='.')
bot.remove_command('help')

@bot.event
async def on_ready():
    print('Bot logged as {}'.format(bot.user))
    logging.info('Bot logged as {}'.format(bot.user))

@bot.event
async def on_message(message):
    log_message.info(f'{message.author} send "{message.content}" to {str(message.channel)}')
    msg = message.content.lower()
    if str(message.author) not in black_list:
        await bot.process_commands(message)

        if msg in dawn:
            await message.channel.send('я твое очко наизнку вертел')

    else:
        if str(message.author) != 'Groovy#7254' and str(message.author) != 'ProBot ✨#5803':
            logging.warning(f'{message.author} send "{message.content}" to {message.channel}')

    try:
        if str(msg)[0] in ban_prefix and str(message.channel).lower() in protect_channel:
            await message.channel.purge(limit=1)
    except IndexError:
        if str(message.author) == 'Groovy#7254' or str(message.author) == 'ProBot ✨#5803':
            await message.channel.purge(limit=1)

@bot.command(pass_context = True)
async def clear(ctx, amount=10):
    if str(ctx.message.author) in admins:
        await ctx.channel.purge(limit=amount+1)
    else: await ctx.channel.send('{0.author.mention} Иди нах :)'.format(ctx.message))


bot.run(token)
