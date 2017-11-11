import os
import requests
import csv
from loader import Loader


loader = Loader(os.path.join(os.path.dirname(
    __file__), '../data/coins.csv'), type='csv')
data = loader.start()


new_data = [
    ['currency', 'live', 'home_page', 'open_source',
        'github', 'owner_name', 'repo_name']
]


temp = None
for d in data[1:, :]:
    name = d[0]
    url = d[1]
    try:
        response = requests.get(url)
        html = response.text.lower()
        if 'https://github.com/' in html:
            # 1. find github url
            first_index = html.find('https://github.com/')
            temp = html[first_index:first_index + 100]
            last_index = temp.find('"')
            link = temp[:last_index]

            # 2. find owner
            link_back = link[link.find('.com/') + 5:]
            owner = link_back[:link_back.find('/')]

            # 3. find repo
            link_back2_idx = link_back.find(owner)
            last_string = link_back[link_back2_idx + len(owner) + 1:]
            link_back2_idx = last_string.find('/')
            repo_name = None
            print('link_back2_idx', link_back2_idx)
            if link_back2_idx == -1:
                repo_name = last_string[:]
            else:
                repo_name = last_string[:link_back2_idx]
            print([name, True, url, True, link, owner, repo_name])
            temp = [name, True, url, True, link, owner, repo_name]
            new_data.append(temp)
        else:
            temp = [name, True, url, False, None, None, None]
            new_data.append([name, True, url, False, None, None, None])
    except (requests.ConnectionError, requests.exceptions.MissingSchema, requests.exceptions.TooManyRedirects):
        temp = [name, False, None, None, None, None, None]
        new_data.append([name, False, None, None, None, None, None])
    with open(os.path.join(os.path.dirname(__file__), '../data/coins_with_repo.csv'), 'a') as f:
        w = csv.writer(f, delimiter=',')
        w.writerow(temp)
