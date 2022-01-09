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
  cy.contains('You are not logged in');
  cy.url().should('include', '/login');
  cy.get('#id_username')
      .type(email)
      .should('have.value', email);
  cy.get('#id_password').type(password);
  cy.get('#submit_button').contains('Log In').click();
};
