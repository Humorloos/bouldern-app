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
    isBusy: false,
    error: '',
  },
  mutations: {
    setBusy: (state) => state.isBusy = true,
    clearBusy: (state) => state.isBusy = false,
    setError: (state, error) => state.error = error,
    clearError: (state) => state.error = '',
    setLoginData: (state, payload) => {
      state.authToken.token = payload.access_token;
      state.authToken.expiration = new Date(payload.access_token_expiration);
      state.refreshToken.token = payload.refresh_token;
      state.refreshToken.expiration =
            new Date(payload.refresh_token_expiration);
      state.user = payload.user;
    },
    clearToken: (state) => {
      state.token = '';
      state.expiration = Date.now();
    },
  },
  getters: {
    isAuthenticated: (state) => state.authToken.token.length > 0 &&
          state.authToken.expiration > Date.now(),
  },
  // actions: {
  //  login: async ({commit}, authenticationData) => {
  //    try {
  //      commit('setBusy');
  //      commit('clearError');
  //      const http = createHttp(false); // unauthenticated
  //      const result = await http.post(
  //          '/registration/rest/login/', authenticationData);
  //      if (result.data.success) {
  //        commit('setToken', result.data);
  //      } else {
  //        commit('setError', 'Authentication Failed');
  //      }
  //    } catch {
  //      commit('setError', 'Failed to login');
  //    } finally {
  //      commit('clearBusy');
  //    }
  //  },
  // },
});
