import os
import json
from numpy import genfromtxt
import pandas as pd


class Loader(object):
    def __init__(self, path, type='json'):
        self.db = path
        self.type = type

    def start(self):
        if self.type == 'json':
            with open(self.db, 'r') as f:
                return json.load(f)
        elif self.type == 'csv':
            # return genfromtxt(self.db, delimiter=',', dtype="|U", quotechar='"')
            return pd.read_csv(self.db, delimiter=',', dtype='|U', quotechar='"').fillna('').values
        elif self.type == 'txt':
            with open(self.db, 'r') as f:
                return f.readlines()
        else:
            print('not support')


def main():
    loader = Loader(os.path.join(os.path.dirname(__file__),
                                 '../data/coin_repo.csv'), type='csv')
    loader.start()


if __name__ == '__main__':
    main()
