import {createStore} from 'vuex';
import messages from '../lang/translations/en';
import http from '../http-common';
const getDefaultState = () => {
  return {
    authToken: {
      token: '',
      expiration: Date.now(),
    },
    refreshToken: {
      token: '',
      expiration: Date.now(),
    },
    user: {
      email: '',
      first_name: '',
      last_name: '',
      pk: 0,
    },
    axios: http,
    messages,
  };
};

export default createStore({
  state: getDefaultState(),
  mutations: {
    setLoginData: (state, payload) => {
      state.authToken.token = payload.access_token;
      state.authToken.expiration = new Date(payload.access_token_expiration);
      state.refreshToken.token = payload.refresh_token;
      state.refreshToken.expiration =
            new Date(payload.refresh_token_expiration);
      state.user = payload.user;
    },
    logout: (state) => {
      // Merge rather than replace so we don't lose observers
      // https://github.com/vuejs/vuex/issues/1118
      Object.assign(state, getDefaultState());
    },
  },
  getters: {
    isAuthenticated: (state) => state.authToken.token.length > 0 &&
          state.authToken.expiration > Date.now(),
  },
});
