/** @file utility functions for use over multiple e2e tests */

import i18n from '../../src/i18n';

window.$t = i18n.global.t;
/**
 * Logs in user with given credentials when at login page
 *
 * @param email the user's email
 * @param password the user's password
 */
window.loginViaLogInLink = (email, password) => {
  cy.contains('You are not logged in');
  cy.url().should('include', '/login');
  cy.get('#id_email')
      .type(email)
      .should('have.value', email);
  cy.get('#id_password').type(password);
  for (const _ of waitingFor('POST', '/registration/login')) {
    cy.get('#submit_button').click();
  }
};

/**
 * Converts the given string into a slug
 * - taken from https://gist.github.com/codeguy/6684588
 *
 * @param str the string to convert
 * @returns {string} the slug
 */
window.slugify = function(str) {
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
};

/**
 * Utility for an API call to finish proceeding. The API call has to occur
 * within a for block using this function.
 * Usage: for (const _ of waitingFor(..., ...)) {...}
 * Source: https://stackoverflow.com/questions/62879698/any-tips-on-context-manager-similar-to-python-in-javascript
 *
 * @param method the method used in the API call
 * @param url the request's target url
 */
window.waitingFor = function* (method, url) {
  // setup
  cy.intercept(method, encodeURI(url)).as('request');
  try {
    yield;
  } finally {
    // cleanup
    cy.wait('@request');
  }
};
