/** @file vuex store configuration */

import {createStore} from 'vuex';
import http from '../http-common';
import i18n from '../i18n';
import createPersistedState from 'vuex-persistedstate';

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
    loginError: '',
    axios: http,
  };
};

export default createStore({
  plugins: [createPersistedState()],
  state: getDefaultState(),
  mutations: {
    /**
     * Sets jwt tokens and user data from the provided payload which contains
     * the server's login response.
     */
    setLoginData(state, loginData) {
      state.authToken.token = loginData.access_token;
      state.authToken.expiration = loginData.access_token_expiration;
      state.refreshToken.token = loginData.refresh_token;
      state.refreshToken.expiration = loginData.refresh_token_expiration;
      state.user = loginData.user;
      state.loginError = '';
    },
    /**
     * Sets the login error message
     */
    setLoginError(state) {
      state.loginError = i18n.global.t('wrongCredentialsMsg');
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
    /**
     * Submits the login form to the login api and commits the returned data to
     * the store. In case of error shows an error message.
     */
    async login({state, commit}, form) {
      try {
        const response = await state.axios.post(
            '/registration/login/', form);
        const loginData = response.data;
        commit('setLoginData', loginData);
      } catch (error) {
        console.log(error);
        commit('setLoginError');
      }
    },
    /**
     * todo
     *
     * @returns {object} Promise for response
     */
    async requestWithJwt({state}, options) {
      const defaultOptions = {
        apiPath: '/',
        method: 'POST',
        data: {},
        contentType: 'application/json',
      };
      Object.keys(defaultOptions).forEach((key) => {
        if (!(key in options)) {
          options[key] = defaultOptions[key];
        }
      });
      return state.axios(options.apiPath, {
        method: options.method,
        data: options.data,
        headers: {
          'authorization': `Bearer ${state.authToken.token}`,
          'content-type': options.contentType,
        },
      });
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
        new Date(state.authToken.expiration) > Date.now();
    },
    state: (state) => state,
  },
});
