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


Cypress.Commands.add('enterNewCredentialsAndLogin', () => {
  cy.get('#id_username')
      .type(Cypress.env('newEmail'))
      .should('have.value', Cypress.env('newEmail'));
  cy.get('#id_password').type(Cypress.env('newPassword'));

  cy.get('#submit_button').contains('Log In').click();
});


Cypress.Commands.add('enterCredentialsAndLogin', () => {
  cy.get('#id_username')
      .type(Cypress.env('email'))
      .should('have.value', Cypress.env('email'));
  cy.get('#id_password').type(Cypress.env('password'));

  cy.get('#submit_button').contains('Log In').click();
});

Cypress.Commands.add('logInViaLogInLink', () => {
  cy.contains('You are not logged in');
  cy.contains('Log In').click();

  cy.url().should('include', '/registration/login');

  cy.enterNewCredentialsAndLogin();
});

Cypress.Commands.add('logInViaLogInLinkNew', () => {
  cy.contains('You are not logged in');

  cy.url().should('include', '/login');

  cy.enterNewCredentialsAndLogin();
});

Cypress.Commands.add('logInViaLogInLinkVue', () => {
  cy.contains('You are not logged in');

  cy.url().should('include', '/login');

  cy.enterCredentialsAndLogin();
});

Cypress.Commands.add('verifyLogInWithInvalidUser', () => {
  cy.logInViaLogInLink();

  cy.contains('Please enter a correct email and password.');
});

Cypress.Commands.add('register', () => {
  cy.get('#id_username')
      .type(Cypress.env('newUsername'))
      .should('have.value', Cypress.env('newUsername'));
  cy.get('#id_email')
      .type(Cypress.env('newEmail'))
      .should('have.value', Cypress.env('newEmail'));
  cy.get('#id_password1').type(Cypress.env('newPassword'));
  cy.get('#id_password2').type(Cypress.env('newPassword'));
  cy.get('#submit_button').contains('Register').click();
});

Cypress.Commands.add('registerAndLogin', () => {
  cy.visit(`${Cypress.env('host')}/registration/signup/`);

  cy.register();

  cy.enterNewCredentialsAndLogin();
});

Cypress.Commands.add('registerAndLoginVue', () => {
  cy.contains('Register').click();
  cy.register();
  cy.contains('Home').click();

  cy.contains('Log In').click();
  // log in with registered user
  cy.logInViaLogInLinkNew();
  cy.contains(`Hello, ${Cypress.env('newEmail')}. ` +
          'You\'re at the bouldern index.');
  cy.contains('Home').click();
});

Cypress.Commands.add('openNewGymMap', () => {
  cy.get('#id_gym-name').type(Cypress.env('newGymName'));
  cy.get('#submit_button').click();
  cy.wait(500);
});

Cypress.Commands.add('openGymMap', () => {
  cy.get('#id_gym-name').type(Cypress.env('gymName'));
  cy.get('#submit_button').click();
  cy.wait(500);
});
