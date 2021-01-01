from dataclasses import dataclass


@dataclass
class Data:
    # default data
    messages = {"greetings": ['Хэй!Это же {}, тот самый,ну ебанутый.ОН ТЕПЕРЬ С НАМИ.ЮХУУУУ!!!', 'Добро пожаловать, {}',
                              'Привет, {}', 'Хэй! Это ты,{}, вчера ту телку ебал?',
                              'Еьать, блудной сын вернулся, как дела {}?', 'Здарова, {}'], }
    channels = {'unprotect_channels': [660217116414312449], }
    head_admins = [472752967745798145, 412477813418098699]
    urls = ['https://vk.com/oryslenti', 'https://vk.com/public171746659',
            'https://vk.com/nestandartniememi', 'https://vk.com/chlgpro',
            'https://vk.com/shkolkrim']
    vk_token = ''
    vk_mail = {
        'meme': {'channel_id': 761600162501754910, 'time': 10,
                 'group_ids': ['nestandartniememi', 'damngenius', 'shkolkrim', ]},
    }
