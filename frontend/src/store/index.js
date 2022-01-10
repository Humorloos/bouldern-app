/** @file vuex store configuration */

import {createStore} from 'vuex';
import http from '../http-common';
import i18n from '../i18n';
import {Storage} from '@ionic/storage';

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
    ionicStorage: {},
  };
};

export default createStore({
  state: getDefaultState(),
  mutations: {
    /**
     * Sets jwt tokens and user data from the provided payload which contains
     * the server's login response.
     */
    setLoginData(state, loginData) {
      // debugger;
      state.authToken.token = loginData.access_token;
      state.authToken.expiration = new Date(loginData.access_token_expiration);
      state.refreshToken.token = loginData.refresh_token;
      state.refreshToken.expiration =
        new Date(loginData.refresh_token_expiration);
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
     * Mounts the ionic storage to the state
     */
    setIonicStorage(state, storage) {
      state.ionicStorage = storage;
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
            '/registration/rest/login/', form);
        const loginData = response.data;
        commit('setLoginData', loginData);
        // await storage.set('user', JSON.stringify(loginData.user));
        for (const key of Object.keys(loginData)) {
          await state.ionicStorage.set(key, JSON.stringify(loginData[key]));
        }
      } catch (error) {
        console.log(error);
        commit('setLoginError');
      }
    },
    /**
     * Loads the data stored in ionic storage and logs in with it if possible
     */
    async loginFromStorage({commit}) {
      const storage = await new Storage().create();
      commit('setIonicStorage', storage);
      const keys = await storage.keys();
      const storageData = {};
      for (const key of keys) {
        const value = await storage.get(key);
        storageData[key] = JSON.parse(value);
      }
      if (keys.length > 0) {
        commit('setLoginData', storageData);
      }
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
