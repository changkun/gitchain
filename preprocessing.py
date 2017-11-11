import json
from utils import parser

rows = []

parser = parser.Parser('../data/bitcoin-bitcoin-commits.logs')
print(parser.count_commits())


with open('/Users/xueguoliang/gitchain/data/bitcoin-bitcoin.json') as json_file:
    record = json.load(json_file)

    # get the feature from raw data
    row = str(record["id"]) + "," + \
          str(record["stargazers_count"]) + "," + \
          str(record["watchers_count"]) + "," + \
          str(record["forks_count"]) + "," + \
          str(record["watchers"]) + "," + \
          str(len(record["contributors"])) + "," + \
          str(len(record["contributors"])) + "," + \
          str(record["open_issues_count"]) + "," + \
          str(record["created_at"]) + "," + \
          str(record["size"])

    rows.append(row)

print(rows)




