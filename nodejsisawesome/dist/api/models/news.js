'use strict';

Object.defineProperty(exports, "__esModule", {
  value: true
});

var _mongoose = require('mongoose');

var _mongoose2 = _interopRequireDefault(_mongoose);

function _interopRequireDefault(obj) { return obj && obj.__esModule ? obj : { default: obj }; }

exports.default = _mongoose2.default.model('News', new _mongoose2.default.Schema({
  timestamp: {
    type: Date,
    required: true
  },
  currency: {
    type: String,
    required: true
  },
  correlation: {
    type: Number,
    required: true
  }
}));
//# sourceMappingURL=news.js.map