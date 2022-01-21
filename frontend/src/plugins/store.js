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
    activeGym: 'generic_gym',
  };
};

export default createStore({
  plugins: [createPersistedState()],
  state: getDefaultState(),
  mutations: {
    setActiveGym(state, gymName) {
      state.activeGym = gymName;
    },
    setUser(state, user) {
      state.user = user;
    },
    setAuthToken(state, authToken) {
      state.authToken = authToken;
    },
    setRefreshToken(state, refreshToken) {
      state.refreshToken = refreshToken;
    },
    setAuthTokenToken(state, authTokenToken) {
      state.authToken.token = authTokenToken;
    },
    /**
     * Sets the login error message
     */
    setLoginError(state) {
      state.loginError = i18n.global.t('wrongCredentialsMsg');
    },
    /**
     * clears the login error message
     */
    clearLoginError(state) {
      state.loginError = '';
    },
    /**
     * Resets the state to default.
     */
    logout(state) {
      // Merge rather than replace so we don't lose observers
      // https://github.com/vuejs/vuex/issues/1118
      Object.assign(state, getDefaultState());
    },
  },
  actions: {
    /**
     * Sends delete request for currently logged-in account
     */
    deleteAccount({state, dispatch}) {
      dispatch('requestWithJwt', {
        apiPath: `/registration/user/${state.user.pk}/`,
        method: 'DELETE',
      });
    },
    /**
     * Calls deleteAccount and logout mutations
     */
    deleteAccountAndLogout({commit, dispatch}) {
      dispatch('deleteAccount');
      commit('logout');
    },
    /**
     * Sets jwt tokens and user data from the provided payload which contains
     * the server's login response.
     */
    setLoginData({state, commit}, loginData) {
      commit('setAuthToken', {
        token: loginData.access_token,
        expiration: loginData.access_token_expiration,
      });
      commit('setRefreshToken', {
        token: loginData.refresh_token,
        expiration: loginData.refresh_token_expiration,
      });
      commit('setUser', loginData.user);
      commit('clearLoginError');
    },
    /**
     * Submits the login form to the login api and commits the returned data to
     * the store. In case of error shows an error message.
     */
    async login({state, commit, dispatch}, form) {
      try {
        const response = await state.axios.post(
            '/registration/login/', form);
        const loginData = response.data;
        dispatch('setLoginData', loginData);
      } catch (error) {
        console.log(error);
        commit('setLoginError');
      }
    },
    /**
     * Makes an authorized request to the specified path with the specified
     * method, data, and content type. If the auth token is expired, and there
     * is a valid refresh token, first refreshes the auth token before the
     * request.
     *
     * @param store the vuex store
     * @param store.state the vuex store's state
     * @param store.getters the vuex store's getters
     * @param store.commit the vuex store's mutations
     * @param options the request specification
     * @param options.apiPath the url to which to send the request to
     * @param [options.method=POST] the http method to use for the request
     * @param [options.data={}] the data to send in the request
     * @param [options.contentType=application/json] the content type to be
     * specified in the contentType header
     * @returns {object} Promise for response
     */
    async requestWithJwt({state, getters, commit}, options) {
      // set options
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
      // if necessary, refresh authToken
      if (!getters.hasValidAuthToken) {
        if (getters.hasValidRefreshToken) {
          const refreshResponse = await state.axios.post(
              '/registration/token/refresh/', {
                refresh: state.refreshToken.token,
              });
          commit('setAuthToken', {
            token: refreshResponse.data.access,
            expiration: refreshResponse.data.access_token_expiration,
          });
        }
      }
      // make api call
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
    hasValidAuthToken(state) {
      return state.authToken.token.length > 0 &&
        new Date(state.authToken.expiration) > Date.now();
    },
    /**
     * Whether the refresh token is set and not expired
     *
     * @returns {boolean} whether the refresh token is set and not expired
     */
    hasValidRefreshToken(state) {
      return state.refreshToken.token.length > 0 &&
        new Date(state.refreshToken.expiration) > Date.now();
    },
    /**
     * Whether the user is authenticated
     *
     * @returns {boolean} whether the user is authenticated
     */
    isAuthenticated(state, getters) {
      return getters.hasValidRefreshToken || getters.hasValidAuthToken;
    },
    state: (state) => state,
  },
});
