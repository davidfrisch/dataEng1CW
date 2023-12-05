import axios from 'axios';
import { FLASK_URL } from '../constants.js';

export default axios.create({
  baseURL: FLASK_URL,
  timeout: 1000,
  headers: {
    'Content-Type': 'application/json',
  },
});

