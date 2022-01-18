/** @file test for registration, login, logout, and account deletion */

import GymMapView from '@/views/GymMap';

after(() => {
  cy.task('log', Object.keys(cy.$log));
  cy.writeFile('cypress/logs/vuex.json', cy.$log);
});

describe('The register app', () => {
  it.only('refreshes auth token after expiration', () => {
    let loginData;
    cy.request('POST', 'https://localhost:8000/registration/login/', {
      username: constants.email,
      password: constants.password,
    }).its('body')
        .then((res) => {
          loginData = res;
        });
    cy.visit('', {
      onLoad: (win) => {
        win.$store.dispatch('setLoginData', loginData);
      },
    });
    cy.window().its('$store.state.authToken.token').should('not.be.empty');
    cy.visit('login');
    // remove auth token
    cy.window().then((win) => win.$store.commit('setAuthTokenToken', ''));
    cy.visit(`gym-map/${constants.gymName}`);
    cy.window().its(`${GymMapView.name}.$data.loaded`).should('equal', true);
  });

  it('shows an error message when trying to log in with wrong crendentials',
      () => {
        cy.visit('');
        cy.contains('Log In').click();
        // try log in with non-existent user
        loginViaLogInLink(constants.newEmail, constants.newPassword);
        cy.contains($t('wrongCredentialsMsg'));
      });

  it('allows logging in after registration', () => {
    cy.visit('');
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
  });

  it('stays logged in after reloading the page', () => {
    cy.visit('login');
    loginViaLogInLink(constants.email, constants.password);
    // log in with registered user
    cy.contains($t('welcomeMsg', {user: constants.email}));
    cy.reload();
    cy.contains(`Hello, ${constants.email}. ` +
      'You\'re at the bouldern index.');
  });

  it('allows logging out', () => {
    cy.visit('login');
    loginViaLogInLink(constants.email, constants.password);
    // log in with registered user
    cy.contains($t('welcomeMsg', {user: constants.email}));
    cy.contains('Home').click();
    cy.contains('Log Out').click();
    cy.contains('Log In').click();
    cy.contains($t('notLoggedInMsg'));
  });

  it('allows deleting ones account', () => {
    cy.visit('login');
    loginViaLogInLink(constants.email, constants.password);
    cy.contains($t('welcomeMsg', {user: constants.email}));
    cy.contains('Home').click();
    cy.contains('Delete Account').click();
    cy.contains('Log In').click();
    loginViaLogInLink(constants.email, constants.password);
    cy.contains($t('wrongCredentialsMsg'));
  });
});
