import json
from utils import parser
import glob
import os
from collections import Counter
from datetime import datetime
from tqdm import tqdm

def unix_time(dt):
    epoch = datetime.utcfromtimestamp(0).date()
    delta = dt - epoch
    return delta.total_seconds()

def span(start):
    now = datetime.now()
    period = (now - datetime.strptime(start, "%Y-%m-%d")).days
    return period

f = open('data/features.csv', 'w')
f.write("name" + "," + "commit_count" + "," + "star_count" + "," + "watcher_count" + "," + "forks_count" + "," + "contributers_count" + "," + "open_issues_count" + "," + "subscribers_count"+ "," +"period" +"\n")

c = open('data/commits.csv', 'w')
c.write("name" + "," + "time" + ","  "value" + "\n")

for coin in tqdm(glob.glob("data/*.json")):

    basename = os.path.splitext(coin)[0].split("/")[-1]

    log = parser.Parser("../data/"+basename+"-commits.logs")
    commit_count, dates = log.count_commits()

    #number of commits per day
    formed_dates = []

    for date in dates:
        formed_date = datetime.strptime(date, "%a %b %d %H:%M:%S %Y %z").date()
        formed_dates.append(formed_date)

    commits_per_day = dict(Counter(formed_dates))

    # parse the json file
    json_file = open(coin)
    record = json.load(json_file)

    #calculate the period
    date_ = record["created_at"].split("T")[0]
    period = span(date_)

     # get the feature from raw data
    coin = str(record["name"]) + "," + \
          str(commit_count) + "," + \
          str(record["stargazers_count"]) + "," + \
          str(record["watchers_count"]) + "," + \
          str(record["forks_count"]) + "," + \
          str(len(record["contributors"])) + "," + \
          str(record["open_issues_count"]) + "," + \
          str(record["subscribers_count"]) + "," + \
          str(period)

    f.write(coin + "\n")

    for x in set(formed_dates):
        time_integer = int(unix_time(x))
        commit = str(record["name"]) + "," + str(time_integer) + "," + str(commits_per_day[x])
        c.write(commit + "\n")

c.close()
f.close()

