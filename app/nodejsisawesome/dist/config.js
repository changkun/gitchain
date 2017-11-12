"use strict";

Object.defineProperty(exports, "__esModule", {
  value: true
});
var config = {
  "port": 8080,
  "bodyLimit": "100kb",
  "corsHeaders": ["Link"],
  api: {
    news: {
      path: '../data',
      csv: {
        headers: true
      },
      fileFormat: {
        repoOverview: 'coins_with_repo.csv',
        repo: '{OWNER}-{PROJECT}.json',
        commits: '{OWNER}-{PROJECT}-commits.log'
      }
    }
  }
};

exports.default = config;
//# sourceMappingURL=config.js.map