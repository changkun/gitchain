import json
from utils.parser import Parser

rows = []

parser = Parser('../data/bitcoin-bitcoin-commits.logs')
print(parser.count_commits())

# get the commit number
#with open("/Users/xueguoliang/gitchain/data/bitcoin-bitcoin-commits.logs") as log_file:

#    for line in log_file.readlines():
 #       match = re.search(r'commit [\w]+', line)
 #   print(match)


with open('/Users/xueguoliang/gitchain/data/bitcoin-bitcoin.json') as json_file:
    data = json.load(json_file)
for record in data:
    # get the feature from raw data
    row = record["id"] + "," + \
          record["stargazers_count"] + "," + \
          record["watchers_count"] + "," + \
          record["forks_count"] + "," + \
          record["watchers"] + "," + \
          len(record["contributors"]) + "," + \
          record["open_issues_count"] + "," + \
          record["created_at"] + "," + \
          record["size"]
    #rows.append(row)






