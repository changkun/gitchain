import os
from creeper import RepoSpider
from loader import Loader

loader = Loader(os.path.join(os.path.dirname(__file__),
                             '../data/coins_with_repo.csv'), type='csv')
data = loader.start()
for d in data[1:, -2:]:
    owner = d[0] if d[0] != '' else None
    repo = d[1] if d[1] != '' else None
    if owner != None and repo != None:
        spider = RepoSpider(owner, repo)
        spider.start()
    else:
        continue
