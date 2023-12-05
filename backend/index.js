import express from 'express';
import cors from 'cors';
import helmet from 'helmet';
import { ResultsProteinsRouter } from './routes/runs.js';

const app = express();
app.use(cors());
app.use(helmet());

app.get('/', (req, res) => {
  res.send('Hello World!');
});

app.use('/runs', ResultsProteinsRouter);

app.listen(3001, () => {
  console.log('Server is listening on port 3001');
});