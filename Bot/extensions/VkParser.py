from itertools import groupby, chain
from random import randint

import vk

from Bot.data.Data import Data


class VkParser:
    def __init__(self, group_ids=None):
        self.version_api = 5.126
        self.group_ids = group_ids
        self.token = Data.vk_token
        self.session = vk.Session(access_token=self.token)
        self.api = vk.API(self.session, lang=0, v=5.126)
        self.cached_posts = []

    def posts(self):
        p = list(chain(*[self.get_posts(gr) for gr in self.group_ids]))
        return p

    def get_posts(self, domain, count=4, atts_max = 1):
        def _data_append(group_id, date, content):
            data.append(
                {'group_id': group_id, 'date': date,
                 'content': content})
        data = []
        for i in range(count):
            self.group_id = group_id = self.api.utils.resolveScreenName(screen_name=domain)['object_id']
            first = self.api.wall.get(owner_id=f'-{group_id}')
            items = first['items'][i]
            # print(domain)
            # check it to ads, is post pinned, audio
            if 'attachments' in items and any(['copyright' in items, items['marked_as_ads'] == 1, 'is_pinned' in items,
                    'video' in items['attachments'][0],
                    any(['audio' in i for i in items["attachments"]], ),
                    'video' in items]):
                continue
            elif 'attachments' not in items:
                _data_append(group_id,date=items['date'], content={'text':items['text'], 'attachments':''})
            else:
                text = items['text']
                # if :
                #     print('Fuck')
                attachments = self.get_photo(items['attachments']) if 'attachments' in items else None
                if len(attachments) <= atts_max:
                    _data_append(**
                        {'group_id': group_id, 'date': items['date'],
                         'content': {'text': text, 'attachments': attachments}})
                else:
                    continue

        return data

    def get_photo(self, attachments):
        urls = []
        for a in attachments:
            # sort by size
            a = a['photo']['sizes']
            group_data = self.group_sorted(a, key=lambda x: x['height'])
            urls.append([list(grp) for key, grp in group_data][-1][0]['url'])

        return urls

    @staticmethod
    def group_sorted(iterable, key=None):
        return groupby(sorted(iterable, key=key), key=key)

# posts = list(chain(*[VkParser().get_posts(l) for l in lst]))
# print(posts)

