/** @file vuex store configuration */

import {createStore} from 'vuex';
import http from '../http-common';

/**
 * Generates default state of store for initialization
 *
 * @returns {object} the store's default state
 */
const getDefaultState = function() {
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
    /**
     * Sets jwt tokens and user data from the provided payload which contains
     * the server's login response.
     */
    setLoginData(state, payload) {
      state.authToken.token = payload.access_token;
      state.authToken.expiration = new Date(payload.access_token_expiration);
      state.refreshToken.token = payload.refresh_token;
      state.refreshToken.expiration =
        new Date(payload.refresh_token_expiration);
      state.user = payload.user;
    },
    /**
     * Resets the state to default.
     */
    logout(state) {
      // Merge rather than replace so we don't lose observers
      // https://github.com/vuejs/vuex/issues/1118
      Object.assign(state, getDefaultState());
    },
    /**
     * Sends delete request for currently logged-in account
     */
    deleteAccount(state) {
      state.axios.delete(`/registration/user/${state.user.pk}/`, {
        headers: {
          'authorization': `Bearer ${state.authToken.token}`,
        },
      });
    },
  },
  actions: {
    /**
     * Calls deleteAccount and logout mutations
     */
    deleteAccountAndLogout({commit}) {
      commit('deleteAccount');
      commit('logout');
    },
  },
  getters: {
    /**
     * Whether the authtoken is set and not expired
     *
     * @returns {boolean} whether the authtoken is set and not expired
     */
    isAuthenticated(state) {
      return state.authToken.token.length > 0 &&
        state.authToken.expiration > Date.now();
    },
  },
});
