import mongoose from 'mongoose';

export default mongoose.model('News', new mongoose.Schema({
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