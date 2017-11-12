import http from 'http';
import express from 'express';
import cors from 'cors';
import morgan from 'morgan';
import bodyParser from 'body-parser';
import initializeDb from './db';
import config from './config';
import dataFetcher from './api/scripts/importNewsToDb';

let app = express();
app.server = http.createServer(app);

// logger
app.use(morgan('dev'));

// 3rd party middleware
app.use(cors({
  exposedHeaders: config.corsHeaders
}));

app.use(bodyParser.json({
  limit: config.bodyLimit
}));

// connect to db
initializeDb(db => {

  dataFetcher.then(data => {
    console.log('data is fetched');
// api router
    const formattedData = {};
    Object.keys(data).forEach(dataKey => {
      formattedData[dataKey] = {
        score: data[dataKey].score,
        hot: data[dataKey].score > 1
      };
    });
    app.get('/api', function (req, res) {
      res.json(formattedData);
    });

    app.server.listen(process.env.PORT || config.port, () => {
      console.log(`Started on port ${app.server.address().port}`);
    });
  });
});

export default app;