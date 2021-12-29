import axios from 'axios';

export default axios.create({
  baseURL: process.env.NODE_ENV === 'production' ?
        // signals to django-webpack-loader to fall back to Django's standard
        // static finder behavior
        'https://humorloos.pythonanywhere.com/' :
        'https://127.0.0.1:8000/', // in development, use own webpack development server,
  headers: {
    'Content-type': 'application/json',
  },
});
