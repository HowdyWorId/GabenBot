import time
from discord.ext import commands
from Bot.extensions.VkParser import VkParser
from Bot.data import Data

vk = VkParser(atts_max=int)
def vk_mailing():
    while True:
        print(vk.get_random_post())
        time.sleep(1)
vk_mailing()
# vk_mailing()