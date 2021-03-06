/** @file vuex store configuration */

import {createStore} from 'vuex';
import http from '../http-common';
import createPersistedState from 'vuex-persistedstate';
import {Colors} from '../constants/color.js';
import i18n from '../i18n';

const $t = i18n.global.t;

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
      id: -1,
      email: '',
      username: '',
    },
    axios: http,
    favoriteGyms: [],
    gymNames: [],
    colors: [],
    loading: false,
    notifications: [],
    globalAlerts: [],
  };
};

export default createStore({
  plugins: [createPersistedState()],
  state: getDefaultState(),
  mutations: {
    setUser(state, user) {
      state.user = user;
    },
    setAuthToken(state, authToken) {
      state.authToken = authToken;
    },
    setRefreshToken(state, refreshToken) {
      const expiration = JSON.parse(decodeURIComponent(atob(refreshToken
          .split('.')[1]
          .replace(/-/g, '+')
          .replace(/_/g, '/'))
          .split('')
          .map((c) => '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2))
          .join(''))).exp * 1000;
      state.refreshToken = {
        token: refreshToken,
        expiration: expiration,
      };
    },
    setAuthTokenToken(state, authTokenToken) {
      state.authToken.token = authTokenToken;
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
     * Adds the gym with the given name to the list of favorite gyms
     */
    addFavoriteGym(state, gymName) {
      state.favoriteGyms.push(gymName);
    },
    /**
     * Adds the provided notification to the list of notifications
     */
    addNotification(state, notification) {
      state.notifications.push(notification);
    },
    /**
     * Removes the provided notification from the list of notifications
     */
    removeNotification(state, notification) {
      const index = state.notifications.indexOf(notification);
      state.notifications.splice(index, 1);
    },
    /**
     * Removes the provided alert from the list of global alerts
     */
    removeAlert(state, alert) {
      const index = state.globalAlerts.indexOf(alert);
      state.globalAlerts.splice(index, 1);
    },
    /**
     * Adds the provided alert to the list of global alerts
     */
    showAlert(state, alert) {
      if (state.globalAlerts.indexOf(alert) === -1) {
        state.globalAlerts.push(alert);
      }
    },
    /**
     * Clears all global alerts
     */
    clearAlerts(state) {
      state.globalAlerts = [];
    },
    /**
     * Removes the gym with the given name from the favorite gyms
     */
    removeFavoriteGym(state, gymName) {
      if (state.favoriteGyms.includes(gymName)) {
        state.favoriteGyms.splice(state.favoriteGyms.indexOf(gymName), 1);
      }
    },
    /**
     * Removes the gym with the given name from the favorite gyms
     */
    removeGym(state, gymName) {
      state.gymNames.splice(state.gymNames.indexOf(gymName), 1);
    },
    /**
     * Sets the favorite gyms to the provided ones
     */
    setFavoriteGyms(state, loadedFavorites) {
      state.favoriteGyms = loadedFavorites;
    },
    /**
     * Adds the provided gym name to the list of gym names
     */
    addGymName(state, gymName) {
      state.gymNames.push(gymName);
    },
    /**
     * Sets the list of gym names to the provided value
     */
    setGymNames(state, loadedNames) {
      state.gymNames = loadedNames;
    },
    /**
     * Sets the colors to the provided ones
     */
    setColors(state, loadedColors) {
      state.colors = loadedColors;
    },
    /**
     * Adds the provided color to colors
     */
    addColor(state, color) {
      state.colors.push(color);
    },
    /**
     * Shows/hides the loading animation
     */
    setLoading(state, loading) {
      state.loading = loading;
    },
  },
  actions: {
    /**
     * Creates a favorite gym entry for the gym with the provided name and adds
     * it to the favorite gyms
     */
    async addFavoriteGym({dispatch, commit}, gymName) {
      await dispatch('requestWithJwt', {
        apiPath: '/bouldern/favorite-gym/',
        data: {gym: gymName},
      });
      commit('addFavoriteGym', gymName);
    },
    /**
     * Removes the favorite gym entry for the gym with the provided name from
     * the api and the favorite gym list
     */
    async removeFavoriteGym({dispatch, commit}, gymName) {
      await dispatch('requestWithJwt', {
        apiPath: `/bouldern/favorite-gym/${gymName}/`,
        method: 'DELETE',
      });
      commit('removeFavoriteGym', gymName);
    },
    /**
     * Deletes the gym with provided name via API and removes it from favorites
     * and gym list
     */
    async deleteGym({dispatch, commit}, {name, id}) {
      await dispatch('requestWithJwt', {
        apiPath: `/bouldern/gym/${id}/`,
        method: 'DELETE',
      });
      commit('removeGym', name);
      commit('removeFavoriteGym', name);
      dispatch('showTemporaryNotification', {
        message: $t('gymMap.gymDeleted'),
        closable: true,
      });
    },
    /**
     * Loads all favorite gyms via API and saves them to the favorite gym list
     */
    async loadFavoriteGyms({dispatch, commit}) {
      const response = await dispatch('requestWithJwt', {
        apiPath: '/bouldern/favorite-gym/',
        method: 'GET',
      });
      commit('setFavoriteGyms', response.data.map(({gym}) => gym));
    },
    /**
     * Loads all favorite gyms via API and saves them to the favorite gym list
     */
    async loadGymNames({dispatch, commit}) {
      const response = await dispatch('requestWithJwt', {
        apiPath: '/bouldern/gym/',
        method: 'GET',
      });
      commit('setGymNames', response.data.map(({name}) => name));
    },
    /**
     * Loads all available colors from the API and saves them
     */
    async loadColors({dispatch, commit}) {
      const colorResponse = await dispatch('requestWithJwt', {
        method: 'GET',
        apiPath: `/bouldern/color/`,
      });
      commit('setColors', colorResponse.data);
    },
    /**
     * De-activates currently logged-in account
     */
    async deleteAccount({state, dispatch}) {
      await dispatch('requestWithJwt', {
        apiPath: `/registration/user/${state.user.id}/`,
        method: 'DELETE',
      });
    },
    /**
     * Calls deleteAccount and logout mutations
     */
    async deleteAccountAndLogout({commit, dispatch}) {
      await dispatch('deleteAccount');
      commit('logout');
      dispatch('showTemporaryNotification', {
        message: $t('profile.accountDeleted'),
        closable: true,
      });
    },
    /**
     * Sets jwt tokens and user data from the provided payload which contains
     * the server's login response.
     */
    setLoginData({commit}, loginData) {
      commit('setAuthToken', {
        token: loginData.access_token,
        expiration: loginData.access_token_expiration,
      });
      commit('setRefreshToken', loginData.refresh_token);
      commit('setUser', loginData.user);
    },
    /**
     * Submits the login form to the login api and commits the returned data to
     * the store. In case of error shows an error message.
     */
    async login({state, dispatch}, form) {
      let response;
      for (const _ of await dispatch('showingSpinner')) {
        response = await state.axios.post('/registration/login/', form);
      }
      const loginData = response.data;
      dispatch('setLoginData', loginData);
      dispatch('loadGymNames');
      dispatch('loadFavoriteGyms');
      dispatch('loadColors');
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
     * @param store.dispatch the vuex store's actions
     * @param options the request specification
     * @param options.apiPath the url to which to send the request to
     * @param [options.method=POST] the http method to use for the request
     * @param [options.data={}] the data to send in the request
     * @param [options.contentType=application/json] the content type to be
     * specified in the contentType header
     * @returns {object} Promise for response
     */
    async requestWithJwt({state, getters, commit, dispatch}, options) {
      let response;
      for (const _ of await dispatch('showingSpinner')) {
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
            commit('setRefreshToken', refreshResponse.data.refresh);
          }
        }
        // make api call
        response = await state.axios(options.apiPath, {
          method: options.method,
          data: options.data,
          headers: {
            'authorization': `Bearer ${state.authToken.token}`,
            'content-type': options.contentType,
          },
        });
      }
      return response;
    },
    /**
     * Context manager for executing code while showing the loading spinner
     * animation
     */
    * showingSpinner({commit}) {
      commit('setLoading', true);
      try {
        yield;
      } finally {
        commit('setLoading', false);
      }
    },
    /**
     * Adds the provided notification to the list of notifications for 5 seconds
     * and removes it afterwards
     */
    showTemporaryNotification({commit}, notification) {
      commit('addNotification', notification);
      setTimeout(() => commit('removeNotification', notification), 5000);
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
    /**
     * Gets the color object with the provided id
     *
     * @returns {function(*)} function that returns the respective color or the
     * default color if none is found
     */
    colorById(state) {
      return (colorId) => {
        return state.colors.find((c) => c.id === colorId) ||
          Colors.DEFAULT_COLOR;
      };
    },
    state: (state) => state,
  },
});
