/** @file utility functions for use over multiple e2e tests */

import i18n from '../../src/i18n';
import GymMapView from '../../src/views/GymMap.vue';
import {NEW_GYM_NAME} from './constants.js';

window.$t = i18n.global.t;

/**
 * Logs in user with given credentials when at login page
 *
 * @param email the user's email
 * @param password the user's password
 * @param success whether the login is supposed to be successful
 */
export function loginViaLogInLink(email, password, success=true) {
  cy.contains('You are not logged in');
  cy.url().should('include', '/login');
  cy.get('#id_email')
      .type(email)
      .should('have.value', email);
  cy.get('#id_password').type(password);
  for (const _ of waitingFor('/registration/login', success)) {
    cy.get('#submit_button').click();
  }
}

/**
 * Converts the given string into a slug
 * - taken from https://gist.github.com/codeguy/6684588
 *
 * @param str the string to convert
 * @returns {string} the slug
 */
export function slugify(str) {
  str = str.replace(/^\s+|\s+$/g, ''); // trim
  str = str.toLowerCase();

  // remove accents, swap ñ for n, etc
  const from = 'àáäâèéëêìíïîòóöôùúüûñç·/_,:;';
  const to = 'aaaaeeeeiiiioooouuuunc------';
  for (let i = 0, l = from.length; i < l; i++) {
    str = str.replace(new RegExp(from.charAt(i), 'g'), to.charAt(i));
  }

  str = str.replace(/[^a-z0-9 -]/g, '') // remove invalid chars
      .replace(/\s+/g, '-') // collapse whitespace and replace by -
      .replace(/-+/g, '-'); // collapse dashes

  return str;
}

/**
 * Utility for waiting for API calls to finish before proceeding. The API call
 * has to occur within a for block using this function.
 * Usage: for (const _ of waitingFor(...)) {...}
 * Source: https://stackoverflow.com/questions/62879698/any-tips-on-context-manager-similar-to-python-in-javascript
 *
 * @param url the request's target url or an array of target urls to intercept
 * @param success whether the request is supposed to be successful
 */
export function* waitingFor(url, success = true) {
  // setup
  if (!Array.isArray(url)) {
    url = [url];
  }
  const statusCodeRegex = success ? /^2\d{2}/ : /^4\d{2}/;
  url.forEach((u) => cy.intercept(encodeURI(u)).as(u));
  try {
    yield;
  } finally {
    // cleanup
    url.forEach((u) => cy.wait(`@${u}`).its('response.statusCode')
        .should('match', statusCodeRegex));
  }
}

/**
 * Gets the x and y values corresponding to the specified coordinates in the
 * gym map at the time this function is called and calls the provided
 * function with them.
 *
 * @param coordinates the coordinates for which to get the x and y values
 * @param fn the function to call with the x and y values
 * @returns {object} cypress chainable
 */
export function atGymMapCoordinates(coordinates, fn) {
  return cy.window().its(`${GymMapView.name}.map`).then((map) => {
    cy.waitUntil(() => {
      return map.getPixelFromCoordinate(coordinates);
    }).then((pixel) => {
      fn(pixel);
    });
  });
}

/**
 * Asserts that the gym map has finished loading
 */
export function waitForGymMap() {
  cy.window().its(`${GymMapView.name}`).then((map) => {
    cy.waitUntil(() => {
      const loaded = map.loaded;
      map.map.updateSize();
      return loaded;
    });
  });
}

/**
 * Gets the radius of the color style of the boulder at the specified
 * coordinates in the specified map
 *
 * @param gymMap map in which to look for the boulder
 * @param x the x coordinate at which to lok up the boulder
 * @param y the y coordinate at which to lok up the boulder
 * @returns {number} the radius of the boulder's color style
 */
function getBoulderRadius(gymMap, x, y) {
  const boulder = gymMap.getBoulderAtPixel([x, y]);
  if (boulder === undefined) return undefined;
  return boulder.getStyle()[1].getImage().getRadius();
}

/**
 * Checks that the boulder at the specified coordinates in the specified map has
 * the specified radius in its color style
 *
 * @param gymMap the map in which to look up the boulder
 * @param x the x coordinate at which to look up the boulder
 * @param y the y coordinate at which to look up the boulder
 * @param radius the radius the specified boulder is supposed to have
 */
function verifyBoulderRadius(gymMap, x, y, radius) {
  cy.wrap(getBoulderRadius(gymMap, x, y)).should('equal', radius);
}

// options for simulating touch pointer events
const touchPointerOptions = (x, y) => {
  return {x: x, y: y, pointerType: 'touch', pointerId: 1};
};

/**
 * Moves the boulder at coordinates "from" to coordinates "to" via touch pointer
 * interaction and checks that the boulder's radius is changed correctly during
 * the shift
 *
 * @param from the coordinates of the boulder to move
 * @param to the coordinates to which to move the boulder
 */
export function moveBoulder(from, to) {
  cy.window().its(`${GymMapView.name}`).then((gymMap) => {
    atGymMapCoordinates(from, ([x, y]) => {
      cy.get('#id_map-root').trigger('pointerdown', touchPointerOptions(x, y));
      cy.log(`original center: ${getCenter(gymMap)}`);
      cy.log(`current center: ${getCurrentCenter(gymMap)}`);
      cy.waitUntil(() =>
        getBoulderRadius(gymMap, x, y) === gymMap.modifyRadius);
    });
    atGymMapCoordinates(to, ([x, y]) => {
      cy.get('#id_map-root').trigger('pointermove', touchPointerOptions(x, y))
          .trigger('pointerup', touchPointerOptions(x, y)).then(() => {
            verifyBoulderRadius(gymMap, x, y, gymMap.boulderRadius);
          });
    });
  });
}

/**
 * Pans the gym map from its center by the provided number of pixels
 *
 * @param x number of pixels to pan in direction x
 * @param y number of pixels to pan in direction y
 */
export function panMap(x, y) {
  cy.window().then((win) => {
    const xFrom = win.innerWidth / 2;
    const yFrom = win.innerHeight / 2 + 50;
    const xTo = xFrom - x;
    const yTo = yFrom - y;
    cy.get('#id_map-root')
        .trigger('pointerdown', touchPointerOptions(xFrom, yFrom))
        .trigger('pointermove', touchPointerOptions(xFrom + 5, yFrom))
        .trigger('pointermove', touchPointerOptions(xTo, yTo))
        .trigger('pointerup', touchPointerOptions(xTo, yTo));
  });
}

/**
 * Gets the current center of the provided map
 *
 * @param gymMap map to get the center of
 * @returns {number[]} the current map center
 */
export function getCurrentCenter(gymMap) {
  return gymMap.map.frameState_.viewState.center;
}

/**
 * Gets the original center of the provided map
 *
 * @param gymMap map to get the center of
 * @returns {number[]} the original map center
 */
export function getCenter(gymMap) {
  return gymMap.map.getView().getCenter();
}

/**
 * Creates a new boulder with the specified grade at the specified coordinates
 *
 * @param coordinates the coordinates at which to create the boulder
 * @param grade the boulder's grade
 */
export function createBoulder(coordinates, grade) {
  atGymMapCoordinates(coordinates, ([x, y]) => {
    cy.get('#id_map-root').click(x, y);
  });
  cy.get('#id_grade-select').click();
  cy.contains(grade).click();
  for (const _ of waitingFor('/bouldern/gym/1/boulder/')) {
    cy.contains('Save').click();
  }
}

/**
 * Refreshes the gym map via refresh button
 */
export function refreshGymMap() {
  cy.get('.mdi-menu').click();
  for (const _ of waitingFor('/bouldern/gym-map-resources/?name=Generic Gym')) {
    cy.get('#id_refresh').click();
  }
}

/**
 * Logs in the user and loads the master data
 */
export function login() {
  cy.visit('login', {
    onLoad: (win) => {
      win.$store.dispatch('setLoginData', cy.loginData);
    },
  });
  cy.window().its('$store.state.authToken.token').should('not.be.empty');
  for (const _ of waitingFor([
    '/bouldern/favorite-gym',
    '/bouldern/color',
    '/bouldern/gym',
  ])) {
    cy.window().its('$store')
        .then((store) => {
          store.dispatch('loadFavoriteGyms');
          store.dispatch('loadColors');
          store.dispatch('loadGymNames');
        });
  }
}

/**
 * Creates a new gym via the UI
 */
export function createNewGym() {
  cy.log('set name and map');
  cy.get('#id_name').type(NEW_GYM_NAME);
  cy.get('#id_map').attachFile('generic_gym.png');

  cy.log('set grades');
  cy.get('#id_color-grade-1').click();
  cy.contains('Blue').click();
  cy.contains('Add Grade').click();
  cy.get('#id_color-grade-2').click();
  cy.contains('Yellow').click();

  cy.log('set undefined grade');
  cy.get('#id_undefined-grade-active').click();
  cy.get('#id_color-undefined').click();
  cy.contains('Grey').click();

  cy.log('submit');
  for (const _ of waitingFor('/bouldern/gym')) {
    for (const _ of waitingFor('/bouldern/gym/3')) {
      cy.get('#id_save-gym').click();
    }
  }
  waitForGymMap();
}

/**
 * Deletes an account from the profile view
 */
export function deleteAccount() {
  cy.contains($t('profile.deleteAccount')).click();
  cy.contains($t('profile.deleteWarning'));
  cy.contains($t('profile.deleteAccount'));
  for (const _ of waitingFor('/registration/user/*/')) {
    cy.get('#id_delete-account').click();
  }
  cy.contains($t('profile.accountDeleted'));
  cy.get('#id_close-notification-0').click();
}
