import os
import json
import configparser
import requests

# features = {
#     'stars': Int,
#     'forks': Int,
#     'watchings': Int,
#     'contributors': [
#         {
#             'id': Int,
#             'followers': Int,
#             'origin_repos': Int,
#         }
#     ],
#     'issues': Int,
#     'pull_requests': Int,
#     'create_time': Time,
#     'commit_counts': Int
# }


class RepoSpider(object):
    def __init__(self, owner, repo_name):
        config = configparser.ConfigParser()
        config.read(
            os.path.join(
                os.path.dirname(__file__),
                '../config/config.ini'
            )
        )
        username = config.get('AUTH', 'username')
        password = config.get('AUTH', 'password')
        self.owner_name = owner
        self.repo_name = repo_name
        self.repo_url = f'https://api.github.com/repos/{owner}/{repo_name}'
        self.contri_url = f'https://api.github.com/repos/{owner}/{repo_name}/contributors'
        self.auth = (username, password)
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_13_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.89 Safari/537.36'}

        self.db = os.path.join(os.path.dirname(
            __file__), f'../data/{owner}-{repo_name}.json')

    def _exists(self):
        return os.path.isfile(self.db)

    def _writer(self, data):
        with open(self.db, 'w') as json_f:
            json_f.write(json.dumps(data, indent=4, separators=(',', ': ')))
        print('Done.')

    def start(self, clone=True):
        # 0. check data exists or not
        if self._exists():
            print('Exists: ', self.repo_url)
            return
        print('creeping: ', self.repo_url)
        # 1. fetch all repo informations
        repo_response = requests.get(
            url=self.repo_url, auth=self.auth, headers=self.headers)
        print(repo_response)
        repo_infos = json.loads(repo_response.text)
        print(repo_infos)
        if clone:
            os.system(
                f"git clone {repo_infos['clone_url']} temp/{self.repo_name}")
            os.system(
                f'git -C temp/{self.repo_name} log > data/{self.owner_name}-{self.repo_name}-commits.logs')

        # 2. fetch all repo contributors
        contributors = []
        contributors_url = repo_infos['contributors_url']
        # 2.1 fetch first page contributors
        contri_response = requests.get(
            url=self.contri_url, auth=self.auth)
        contributors.append(json.loads(contri_response.text))
        # 2.2 fetch all other contributors
        while True:
            if 'next' in contri_response.links:
                contri_response = requests.get(
                    url=contri_response.links['next']['url'], auth=self.auth)
                contributors.append(json.loads(contri_response.text))
            else:
                contributors.append(json.loads(contri_response.text))
                break

        # 3. write data
        repo_infos['contributors'] = contributors
        self._writer(repo_infos)


def main():
    spider = RepoSpider('bitcoin', 'bitcoin')
    spider.start()


if __name__ == '__main__':
    main()
