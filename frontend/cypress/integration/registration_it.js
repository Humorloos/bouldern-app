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
    cy.window().its(`${GymMapView.name}.$data.loaded`).should('equal', true);
  });

  it('stays logged in after reloading the page', () => {
    // log in with registered user
    cy.contains($t('welcomeMsg', {user: constants.email}));
    cy.reload();
    cy.contains($t('welcomeMsg', {user: constants.email}));
  });

  it('allows logging out', () => {
    cy.contains($t('welcomeMsg', {user: constants.email}));
    cy.get('.mdi-menu').click();
    cy.contains('Log Out').click();
    cy.get('.mdi-menu').click();
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

  it('allows registering, logging in, and deleting ones account ' +
    'afterwards', () => {
    cy.visit('register');

    cy.get('#id_username')
        .type(constants.newUsername)
        .should('have.value', constants.newUsername);
    cy.get('#id_email')
        .type(constants.newEmail)
        .should('have.value', constants.newEmail);
    cy.get('#id_password1').type(constants.newPassword);
    cy.get('#id_password2').type(constants.newPassword);
    cy.intercept('POST', '/registration/').as('register');
    cy.get('.v-form > #submit_button').click();
    cy.wait('@register');

    cy.visit('login');
    loginViaLogInLink(constants.newEmail, constants.newPassword);
    cy.contains($t('welcomeMsg', {user: constants.newEmail}));
    cy.get('.mdi-menu').click();
    cy.contains('Delete Account').click();
    cy.get('.mdi-menu').click();
    loginViaLogInLink(constants.newEmail, constants.newPassword);
    cy.contains($t('wrongCredentialsMsg'));
  });

  it('Redirects to login page when visiting gym map while logged out',
      () => {
        cy.visit(`gym-map/${constants.gymName}`);
        cy.contains($t('notLoggedInMsg'));
      });
});
