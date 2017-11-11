import json
from utils import parser
import glob
import os
from collections import Counter
from datetime import datetime


def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0).date()
    delta = dt - epoch
    return delta.total_seconds()

f = open('data/features.csv', 'a')
f.write("name" + "," + "commit_count" + "," + "star_count" + "," + "watcher_count" + "," + "forks_count" + "," + "contributers_count" + "," + "open_issues_count" + "," + "created_time"+"\n")

result = []

for coin in glob.glob("data/*.json"):

    coin_commit_dict = {}

    basename = os.path.splitext(coin)[0].split("/")[-1]

    log = parser.Parser("../data/"+basename+"-commits.logs")
    commit_count, dates = log.count_commits()

    #number of commits per day
    formed_dates = []
    histories = []

    value = 0

    for date in dates:
        formed_date = datetime.strptime(date, "%a %b %d %H:%M:%S %Y %z").date()
        formed_dates.append(formed_date)

    commits_per_day = dict(Counter(formed_dates))

    for x in set(formed_dates):
        history = {}
        time_integer = int(unix_time(x))
        history["timestamp"] = time_integer
        history["value"] = commits_per_day[x]
        histories.append(history)

    json_file = open(coin)
    record = json.load(json_file)

     # get the feature from raw data
    row = str(record["name"]) + "," + \
          str(commit_count) + "," + \
          str(record["stargazers_count"]) + "," + \
          str(record["watchers_count"]) + "," + \
          str(record["forks_count"]) + "," + \
          str(len(record["contributors"])) + "," + \
          str(record["open_issues_count"]) + "," + \
          str(record["created_at"])

    f.write(row + "\n")

    coin_commit_dict["name"] = str(record["name"])
    coin_commit_dict["commit_history"] = histories

    result.append(coin_commit_dict)

final_data = open("result.json", "w")
final_data.write(json.dumps(result))
final_data.close()

f.close()

