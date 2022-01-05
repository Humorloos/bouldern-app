// ***********************************************
// This example commands.js shows you how to
// create various custom commands and overwrite
// existing commands.
//
// For more comprehensive examples of custom
// commands please read more here:
// https://on.cypress.io/custom-commands
// ***********************************************
//
//
// -- This is a parent command --
// Cypress.Commands.add("login", (email, password) => { ... })
//
//
// -- This is a child command --
// Cypress.Commands
// .add("drag", { prevSubject: 'element'}, (subject, options) => { ... })
//
//
// -- This is a dual command --
// Cypress.Commands
// .add("dismiss", { prevSubject: 'optional'}, (subject, options) => { ... })
//
//
// -- This will overwrite an existing command --
// Cypress.Commands.overwrite("visit", (originalFn, url, options) => { ... })
import 'cypress-file-upload';


Cypress.Commands.add('logInViaLogInLinkNew', () => {
  cy.contains($t('notLoggedInMsg'));

  cy.url().should('include', '/login');

  cy.get('#id_username')
      .type(constants.newEmail)
      .should('have.value', constants.newEmail);
  cy.get('#id_password').type(constants.newPassword);

  cy.get('#submit_button').contains('Log In').click();
});

Cypress.Commands.add('logInViaLogInLink', () => {
  cy.contains('You are not logged in');

  cy.url().should('include', '/login');

  cy.contains('You are not logged in');

  cy.url().should('include', '/login');

  cy.get('#id_username')
      .type(constants.email)
      .should('have.value', constants.email);
  cy.get('#id_password').type(constants.password);

  cy.get('#submit_button').contains('Log In').click();
});
