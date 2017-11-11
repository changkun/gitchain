import re
import os
from utils.loader import Loader


class Parser(object):
    def __init__(self, relative_path):
        self.file = os.path.join(os.path.dirname(__file__), relative_path)
        self.dates = []

    def count_commits(self):
        loader = Loader(self.file, type='txt')
        data = loader.start()
        count = 0
        for line in data:
            if re.match('^(commit )', line):
                count += 1
            if re.match('^(Date: )', line):
                self.dates.append(line.replace("Date:", "").strip())
            else:
                continue
        return count, self.dates


def main():
    parser = Parser('../data/bitcoin-bitcoin-commits.logs')
    print(parser.count_commits())


if __name__ == '__main__':
    main()
