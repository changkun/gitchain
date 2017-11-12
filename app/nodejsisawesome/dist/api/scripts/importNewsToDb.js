'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _fs = require('fs');

var _fs2 = _interopRequireDefault(_fs);

var _fastCsv = require('fast-csv');

var _fastCsv2 = _interopRequireDefault(_fastCsv);

var _path = require('path');

var _path2 = _interopRequireDefault(_path);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var loadRepositories = function loadRepositories() {
  return new Promise(function (resolve, reject) {
    var repositories = {};
    _fs2.default.createReadStream(_path2.default.join(__dirname, "../../../../data/coins_with_repo.csv")).pipe((0, _fastCsv2.default)({
      headers: true
    })).on("data", function (repository) {
      if (repository.open_source === 'True') {
        repositories[repository.currency] = repository;
      }
    }).on("end", function () {
      resolve(repositories);
    });
  });
};

var addNumberOfCommitsToRepositories = function addNumberOfCommitsToRepositories(repositories) {
  var jobs = Object.keys(repositories).map(function (repoKey) {
    return new Promise(function (resolveJob) {
      repositories[repoKey].numberOfCommits = 0;
      var ownerName = repositories[repoKey].owner_name.toLowerCase();
      var repoName = repositories[repoKey].repo_name.toLowerCase();

      try {
        _fs2.default.createReadStream(_path2.default.join(__dirname, '../../../../data/', ownerName + '-' + repoName + '-commits.logs')).on("data", function (dataBunch) {
          dataBunch.toString().split('\n').forEach(function (data) {
            if (data.match(/^(commit )/)) {
              repositories[repoKey].numberOfCommits += 1;
            }

            var isFirstCommit = repositories[repoKey].numberOfCommits === 1;

            if (isFirstCommit && data.match(/(Date:)/)) {
              repositories[repoKey].firstCommitTimestamp = new Date(data.replace('Date:', '').trim());
            }
          });
        }).on("end", function () {
          resolveJob();
        }).on('error', function (e) {
          console.warn('Commit file of ' + _path2.default.join(__dirname, '../../../data/', ownerName + '-' + repoName + '-commits.logs') + ' not found');
          resolveJob();
        });
      } catch (e) {
        console.warn('Commit file of ' + repoName + '-' + ownerName + ' not found');
        resolveJob();
      }
    });
  });

  return Promise.all(jobs).then(function () {
    return Promise.resolve(repositories);
  });
};

var addMetricsFromRepositoryDetailsPage = function addMetricsFromRepositoryDetailsPage(repositories) {
  var jobs = Object.keys(repositories).map(function (repoKey) {
    return new Promise(function (resolveJob) {
      var ownerName = repositories[repoKey].owner_name.toLowerCase();
      var repoName = repositories[repoKey].repo_name.toLowerCase();
      try {
        var repository = require(_path2.default.join(__dirname, '../../../../data/' + ownerName + '-' + repoName + '.json'));

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
    });
  });

  return Promise.all(jobs).then(function () {
    return Promise.resolve(repositories);
  });
};

var addNewsCorrelations = function addNewsCorrelations(repositories) {
  Object.keys(repositories).forEach(function (repositoryName) {
    repositories[repositoryName].news_correlation = 1; // TODO
  });
  return Promise.resolve(repositories);
};

var scoreRepository = function scoreRepository(repository) {
  return repository.firstCommitTimestamp ? 10000000000000000 * ((0.3 * repository.watchers_count + 0.7 * repository.stargazers_count) * 1000 + repository.numberOfCommits) / repository.firstCommitTimestamp.getTime() / 1000 / 60 / 60 / 24 : 0;
};

var weightTheRepositories = function weightTheRepositories(repositories) {
  Object.keys(repositories).forEach(function (repositoryName) {
    repositories[repositoryName].score = scoreRepository(repositories[repositoryName]);
  });

  return Promise.resolve(repositories);
};

var chain = loadRepositories().then(addNumberOfCommitsToRepositories).then(addMetricsFromRepositoryDetailsPage).then(addNewsCorrelations).then(weightTheRepositories);

exports.default = chain;
//# sourceMappingURL=importNewsToDb.js.map