import json
from utils import parser
import glob
import os
from tqdm import tqdm

f = open('features.csv', 'a')
f.write("name" + "," + "commit_count" + "," + "star_count" + "," + "watcher_count" + "," + "forks_count" + "," + "contributers_count" + "," + "open_issues_count" + "," + "created_time"+"\n")

for coin in tqdm(glob.glob("data/*.json")):

    basename = os.path.splitext(coin)[0].split("/")[-1]

    log = parser.Parser("../data/"+basename+"-commits.logs")
    commit_count = log.count_commits()

    with open(coin) as json_file:
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

        f.write(row + "\n")  # python will convert \n to os.linesep

f.close()

