import {createStore} from 'vuex';
import http from '../http-common';

/**
 * Generates default state of store for initialization
 *
 * @returns {object} the store's default state
 */
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
    logout(state) {
      // Merge rather than replace so we don't lose observers
      // https://github.com/vuejs/vuex/issues/1118
      Object.assign(state, getDefaultState());
    },
    deleteAccount(state, payload) {
      state.axios.delete(`/registration/user/${state.user.pk}/`, {
        headers: {
          'authorization': `Bearer ${state.authToken.token}`,
        },
      });
    },
  },
  actions: {
    deleteAccountAndLogout({commit}) {
      commit('deleteAccount');
      commit('logout');
    },
  },
  getters: {
    isAuthenticated: (state) => state.authToken.token.length > 0 &&
            state.authToken.expiration > Date.now(),
  },
});
