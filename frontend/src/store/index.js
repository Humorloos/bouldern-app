import {createStore} from 'vuex';

export default createStore({
  state: {
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
  },
  mutations: {
    setLoginData: (state, payload) => {
      state.authToken.token = payload.access_token;
      state.authToken.expiration = new Date(payload.access_token_expiration);
      state.refreshToken.token = payload.refresh_token;
      state.refreshToken.expiration =
            new Date(payload.refresh_token_expiration);
      state.user = payload.user;
    },
  },
  getters: {
    isAuthenticated: (state) => state.authToken.token.length > 0 &&
          state.authToken.expiration > Date.now(),
  },
});
