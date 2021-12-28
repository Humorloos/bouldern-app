import axios from 'axios';

export default axios.create({
  baseURL: 'https://api.humorloos.pythonanywhere.com:8000',
  headers: {
    'Content-type': 'application/json',
  },
});
