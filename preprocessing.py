import json
from utils import parser

rows = []

first = True

parser = parser.Parser('../data/bitcoin-bitcoin-commits.logs')

f = open('features.csv', 'a')
f.write("name" + "," + "commit_count" + "," + "star_count" + "," + "watcher_count" + "," + "forks_count" + "," + "contributers_count" + "," + "open_issues_count" + "," + "created_time"+"\n")

with open('/Users/xueguoliang/gitchain/data/bitcoin-bitcoin.json') as json_file:
    record = json.load(json_file)

    # get the feature from raw data
    row = str(record["name"]) + "," + \
          str(parser.count_commits()) + "," + \
          str(record["stargazers_count"]) + "," + \
          str(record["watchers_count"]) + "," + \
          str(record["forks_count"]) + "," + \
          str(len(record["contributors"])) + "," + \
          str(record["open_issues_count"]) + "," + \
          str(record["created_at"])

    f.write(row + "\n")  # python will convert \n to os.linesep

f.close()

