import os
from discord.ext import commands

with open('lol.txt', 'r') as f:
    print(f.read())
# token = 'NzAyMTA3OTQ5NDIxODIyMTA0.Xp7O-w.1Kf5hPD5WmvK3YEc3PKJCU_4uXQ'

# client = commands.Bot(command_prefix='.')
# client.remove_command('help')

# cogs_files = [f[:-3] for f in os.listdir('./cogs') if f.endswith('.py')]

# for c in cogs_files:
#     client.load_extension('cogs.{}'.format(c))

# client.run(token)
