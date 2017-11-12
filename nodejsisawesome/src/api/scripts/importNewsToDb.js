import fs from 'fs';
import csv from 'fast-csv';
import path from 'path';

const loadRepositories = () => new Promise((resolve, reject) => {
  const repositories = {};
  fs.createReadStream(path.join(__dirname, "../../../../data/coins_with_repo.csv"))
    .pipe(csv({
      headers: true
    }))
    .on("data", function (repository) {
      if (repository.open_source === 'True') {
        repositories[repository.currency] = repository;
      }
    })
    .on("end", function () {
      resolve(repositories);
    });
});

const addNumberOfCommitsToRepositories = (repositories) => {
  const jobs = Object.keys(repositories).map(function (repoKey) {
    return new Promise(function (resolveJob) {
      repositories[repoKey].numberOfCommits = 0;
      const ownerName = repositories[repoKey].owner_name.toLowerCase();
      const repoName = repositories[repoKey].repo_name.toLowerCase();

      try {
        fs.createReadStream(path.join(__dirname, '../../../../data/', ownerName + '-' + repoName + '-commits.logs'))
          .on("data", function (dataBunch) {
            dataBunch.toString().split('\n').forEach(data => {
              if (data.match(/^(commit )/)) {
                repositories[repoKey].numberOfCommits += 1;
              }

              const isFirstCommit = repositories[repoKey].numberOfCommits === 1;

              if (isFirstCommit && data.match(/(Date:)/)) {
                repositories[repoKey].firstCommitTimestamp = new Date(data.replace('Date:', '').trim());
              }
            });
          })
          .on("end", function () {
            resolveJob();
          })
          .on('error', function (e) {
            console.warn('Commit file of ' + path.join(__dirname, '../../../data/', ownerName + '-' + repoName + '-commits.logs') + ' not found');
            resolveJob();
          });
      } catch (e) {
        console.warn('Commit file of ' + repoName + '-' + ownerName + ' not found');
        resolveJob();
      }
    });
  });

  return Promise.all(jobs).then(() => Promise.resolve(repositories));
};

const addMetricsFromRepositoryDetailsPage = (repositories) => {
  const jobs = Object.keys(repositories).map(repoKey => new Promise(resolveJob => {
    const ownerName = repositories[repoKey].owner_name.toLowerCase();
    const repoName = repositories[repoKey].repo_name.toLowerCase();
    try {
      const repository = require(path.join(__dirname, '../../../../data/' + ownerName + '-' + repoName + '.json'));

      repositories[repoKey].watchers_count = repository.watchers_count;
      repositories[repoKey].stargazers_count = repository.stargazers_count;
      repositories[repoKey].forks_count = repository.forks_count;
      repositories[repoKey].open_issues = repository.open_issues;
      repositories[repoKey].subscribers_count = repository.subscribers_count;
      repositories[repoKey].contributers_count = repository.contributors ? repository.contributors.length : 0;
      repositories[repoKey].realValues = true;
    } catch (e) {
      console.error('Can`t find repository data of name ' + repoName + '. Default values are set');
      repositories[repoKey].watchers_count = 0;
      repositories[repoKey].stargazers_count = 0;
      repositories[repoKey].forks_count = 0;
      repositories[repoKey].open_issues = 0;
      repositories[repoKey].subscribers_count = 0;
      repositories[repoKey].contributers_count = 0;
      repositories[repoKey].realValues = false;
    }
    resolveJob();
  }));

  return Promise.all(jobs).then(() => Promise.resolve(repositories));
};

const addNewsCorrelations = (repositories) => {
  Object.keys(repositories).forEach(repositoryName => {
    repositories[repositoryName].news_correlation = 1; // TODO
  });
  return Promise.resolve(repositories);
};

const scoreRepository = repository => repository.firstCommitTimestamp ?
  10000000000000000 * ((0.3 * repository.watchers_count + 0.7 * repository.stargazers_count) * 1000 + repository.numberOfCommits) / repository.firstCommitTimestamp.getTime() / 1000 / 60 / 60 / 24 : 0;

const weightTheRepositories = (repositories) => {
  Object.keys(repositories).forEach(repositoryName => {
    repositories[repositoryName].score = scoreRepository(repositories[repositoryName]);
  });

  return Promise.resolve(repositories);
};

const chain = loadRepositories()
  .then(addNumberOfCommitsToRepositories)
  .then(addMetricsFromRepositoryDetailsPage)
  .then(addNewsCorrelations)
  .then(weightTheRepositories);

export default chain;
