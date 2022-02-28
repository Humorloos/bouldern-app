/** @file test for registration, login, logout, and account deletion */

import GymMapView from '../../src/views/GymMap.vue';

describe('The register app', () => {
  beforeEach(() => {
    cy.visit('login', {
      onLoad: (win) => {
        win.$store.dispatch('setLoginData', cy.loginData);
      },
    });
    cy.window().its('$store.state.authToken.token').should('not.be.empty');
  });

  it('refreshes auth token after expiration', () => {
    // remove auth token
    cy.window().then((win) => win.$store.commit('setAuthTokenToken', ''));
    cy.visit(`gym-map/${constants.gymName}`);
    cy.window().its(`${GymMapView.name}.loaded`).should('equal', true);
  });

  it('stays logged in after reloading the page', () => {
    cy.visit('profile');
    // log in with registered user
    cy.contains($t('welcomeMsg', {user: constants.username}));
    cy.reload();
    cy.contains($t('welcomeMsg', {user: constants.username}));
  });

  it('allows logging out', () => {
    cy.visit('profile');
    cy.contains($t('welcomeMsg', {user: constants.username}));
    cy.contains('Log Out').click();
    cy.contains($t('notLoggedInMsg'));
  });
});

describe('The register app', () => {
  it('shows an error message when trying to log in with wrong crendentials',
      () => {
        cy.visit('login');
        // try log in with non-existent user
        loginViaLogInLink(constants.newEmail, constants.newPassword);
        cy.contains($t('wrongCredentialsMsg'));
      });

  it('allows registering, logging in, and deleting one\'s account ' +
    'afterwards', () => {
    // register
    cy.visit('register');
    cy.get('#id_username')
        .type(constants.newUsername)
        .should('have.value', constants.newUsername);
    cy.get('#id_email')
        .type(constants.newEmail)
        .should('have.value', constants.newEmail);
    cy.get('#id_password1').type(constants.newPassword);
    cy.get('#id_password2').type(constants.newPassword);
    for (const _ of waitingFor('POST', '/registration/')) {
      cy.get('#submit_button').click();
    }
    cy.contains($t('confirmationEmailAlert', {email: constants.newEmail}));
    // confirm email via confirmation link sent via email
    cy.task('readLastEmail')
        .should('have.string', constants.newEmail.toLowerCase())
        .then((mail) => {
          const confirmationLink = /(https?:\/\/[^\s]+)/g
              .exec(mail)[0]
              .replace('localhost:8000', 'localhost:8080');
          cy.visit(confirmationLink);
        });
    for (const _ of waitingFor('POST', '/registration/verify-email/')) {
      cy.get('#id_confirm_email').click();
    }
    // login with newly created credentials
    cy.visit('login');
    loginViaLogInLink(constants.newEmail, constants.newPassword);
    // check that user is logged in
    cy.visit('profile');
    cy.contains($t('welcomeMsg', {user: constants.newUsername}));
    // delete account
    cy.contains('Delete Account').click();
    // check that logging in with deleted account leads to error message
    loginViaLogInLink(constants.newEmail, constants.newPassword);
    cy.contains($t('wrongCredentialsMsg'));
  });

  it('allows resetting one\'s password', () => {
    cy.visit('reset-password');
    cy.get('#id_email').type(constants.email);
    for (const _ of waitingFor('POST', '/registration/password/reset/')) {
      cy.get('#id_send').click();
    }
    cy.task('readLastEmail')
        .should('have.string', constants.email)
        .then((mail) => {
          const confirmationLink = /(https?:\/\/[^\s]+)/g
              .exec(mail)[0]
              .replace('localhost:8000', 'localhost:8080');
          cy.visit(confirmationLink);
        });
    cy.get('#id_password1').type(constants.password);
    cy.get('#id_password2').type(constants.password);
    for (const _ of waitingFor('POST',
        '/registration/password/reset/confirm/')) {
      cy.get('#id_submit').click();
    }
  });

  it('Redirects to login page when visiting gym map while logged out',
      () => {
        cy.visit(`gym-map/${constants.gymName}`);
        cy.contains($t('notLoggedInMsg'));
      });
});
