/** @file test for registration, login, logout, and account deletion */

import GymMapView from '@/views/GymMap';

after(() => cy.task('log', cy.$log));

describe('The register app', () => {
  it('refreshes auth token after expiration', () => {
    cy.visit('login');
    loginViaLogInLink(constants.email, constants.password);
    cy.window().its('$store.state.authToken.token').should('not.be.empty');
    // remove auth token
    cy.window().then((win) => win.$store.commit('setAuthTokenToken', ''));
    cy.visit(`gym-map/${constants.gymName}`);
    cy.window().its(`${GymMapView.name}.$data.loaded`).should('equal', true);
  });

  it('can register, login, logout, and delete accounts', () => {
    cy.visit('');
    cy.contains('Log In').click();
    // try log in with non-existent user
    loginViaLogInLink(constants.newEmail, constants.newPassword);
    cy.contains($t('wrongCredentialsMsg'));
    cy.contains('Home').click();
    cy.contains('Register').click();

    cy.get('#id_username')
        .type(constants.newUsername)
        .should('have.value', constants.newUsername);
    cy.get('#id_email')
        .type(constants.newEmail)
        .should('have.value', constants.newEmail);
    cy.get('#id_password1').type(constants.newPassword);
    cy.get('#id_password2').type(constants.newPassword);
    cy.get('#submit_button').contains('Register').click();
    cy.contains('Home').click();

    cy.contains('Log In').click();
    loginViaLogInLink(constants.newEmail, constants.newPassword);
    cy.contains(`Hello, ${constants.newEmail}. ` +
          'You\'re at the bouldern index.');

    // after refresh, stay logged in
    cy.reload();
    cy.contains(`Hello, ${constants.newEmail}. ` +
          'You\'re at the bouldern index.');
    cy.contains('Home').click();
    cy.contains('Log Out').click();
    cy.contains('Log In').click();
    cy.contains($t('notLoggedInMsg'));
    // try log in with non-existent user
    loginViaLogInLink(constants.email, constants.password);
    cy.contains('Home').click();
    cy.contains('Delete Account').click();
    cy.contains('Log In').click();
    loginViaLogInLink(constants.email, constants.password);
    cy.contains($t('wrongCredentialsMsg'));
  });
});
