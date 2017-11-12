'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _http = require('http');

var _http2 = _interopRequireDefault(_http);

var _express = require('express');

var _express2 = _interopRequireDefault(_express);

var _cors = require('cors');

var _cors2 = _interopRequireDefault(_cors);

var _morgan = require('morgan');

var _morgan2 = _interopRequireDefault(_morgan);

var _bodyParser = require('body-parser');

var _bodyParser2 = _interopRequireDefault(_bodyParser);

var _db = require('./db');

var _db2 = _interopRequireDefault(_db);

var _config = require('./config');

var _config2 = _interopRequireDefault(_config);

var _importNewsToDb = require('./api/scripts/importNewsToDb');

var _importNewsToDb2 = _interopRequireDefault(_importNewsToDb);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

var app = (0, _express2.default)();
app.server = _http2.default.createServer(app);

// logger
app.use((0, _morgan2.default)('dev'));

// 3rd party middleware
app.use((0, _cors2.default)({
  exposedHeaders: _config2.default.corsHeaders
}));

app.use(_bodyParser2.default.json({
  limit: _config2.default.bodyLimit
}));

// connect to db
(0, _db2.default)(function (db) {

  _importNewsToDb2.default.then(function (data) {
    console.log('data is fetched');
    // api router
    var formattedData = {};
    Object.keys(data).forEach(function (dataKey) {
      formattedData[dataKey] = {
        score: data[dataKey].score,
        hot: data[dataKey].score > 1
      };
    });
    app.get('/api', function (req, res) {
      res.json(formattedData);
    });

    app.server.listen(process.env.PORT || _config2.default.port, function () {
      console.log('Started on port ' + app.server.address().port);
    });
  });
});

exports.default = app;
//# sourceMappingURL=app.js.map