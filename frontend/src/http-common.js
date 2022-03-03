/** @file axios configuration */

import axios from 'axios';

export default axios.create({
  baseURL: import.meta.env.MODE === 'production' ?
        // signals to django-webpack-loader to fall back to Django's standard
        // static finder behavior
        'https://www.boulderholder.com/' :
        'https://localhost:8000/', // in development, use own webpack development server,
  headers: {
    'Content-type': 'application/json',
  },
});
