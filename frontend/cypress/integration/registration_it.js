/** @file test for registration, login, logout, and account deletion */

import GymMapView from '../../src/views/GymMap.vue';
import {
  EMAIL,
  GYM_NAME,
  NEW_EMAIL,
  NEW_PASSWORD,
  NEW_USERNAME,
  PASSWORD,
  USERNAME,
} from '../support/constants.js';
import {loginViaLogInLink, waitingFor} from '../support/functions.js';

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
    cy.visit(`gym-map/${GYM_NAME}`);
    cy.window().its(`${GymMapView.name}.loaded`).should('equal', true);
  });

  it('stays logged in after reloading the page', () => {
    cy.visit('profile');
    // log in with registered user
    cy.contains($t('welcomeMsg', {user: USERNAME}));
    cy.reload();
    cy.contains($t('welcomeMsg', {user: USERNAME}));
  });

  it('allows logging out', () => {
    cy.visit('profile');
    cy.contains($t('welcomeMsg', {user: USERNAME}));
    cy.contains('Log Out').click();
    cy.contains($t('notLoggedInMsg'));
  });

  it('allows registering again after deleting one\'s account', () => {
    cy.log('delete account');
    cy.visit('profile');
    for (const _ of waitingFor('DELETE', '/registration/user/2/')) {
      cy.contains('Delete Account').click();
    }

    cy.log('check that logging in with deleted account leads to error message');
    loginViaLogInLink(EMAIL, PASSWORD);
    cy.contains($t('wrongCredentialsMsg'));

    cy.log('register');
    cy.visit('register');
    cy.get('#id_username').type(USERNAME);
    cy.get('#id_email').type(EMAIL);
    cy.get('#id_password1').type(PASSWORD);
    cy.get('#id_password2').type(PASSWORD);
    for (const _ of waitingFor('POST', '/registration/')) {
      cy.get('#submit_button').click();
    }
    cy.contains($t('msgConfirmationEmailSent', {email: EMAIL}));

    cy.log('confirm email via confirmation link sent via email');
    cy.task('readLastEmail')
        .should('have.string', EMAIL.toLowerCase())
        .then((mail) => {
          const confirmationLink = /(https?:\/\/[^\s]+)/g
              .exec(mail)[0]
              .replace('localhost:8000', 'localhost:8080');
          cy.visit(confirmationLink);
        });
    for (const _ of waitingFor('POST', '/registration/verify-email/')) {
      cy.get('#id_confirm_email').click();
    }

    cy.log('login with newly created credentials');
    cy.visit('login');
    loginViaLogInLink(EMAIL, PASSWORD);
    cy.contains($t('msgEmailConfirmed')).should('not.exist');

    cy.log('check that user is logged in');
    cy.visit('profile');
    cy.contains($t('welcomeMsg', {user: USERNAME}));
  });
});

describe('The login view', () => {
  beforeEach(() => {
    cy.visit('login');
  });

  it('shows an error message when trying to log in with wrong crendentials',
      () => {
        // try log in with non-existent user
        loginViaLogInLink(NEW_EMAIL, NEW_PASSWORD);
        cy.contains($t('wrongCredentialsMsg'));
      });

  it('shows errors when fields are empty', () => {
    cy.get('#submit_button').click();
    ['lblPassword', 'lblEmail'].forEach((key) => {
      cy.contains($t('msgRequiredField', {field: $t(key)}));
    });
  });
});

describe('The register app', () => {
  it('allows resetting one\'s password', () => {
    cy.visit('reset-password');
    cy.get('#id_email').type(EMAIL);
    for (const _ of waitingFor('POST', '/registration/password/reset/')) {
      cy.get('#id_send').click();
    }
    cy.task('readLastEmail')
        .should('have.string', EMAIL)
        .then((mail) => {
          const confirmationLink = /(https?:\/\/[^\s]+)/g
              .exec(mail)[0]
              .replace('localhost:8000', 'localhost:8080');
          cy.visit(confirmationLink);
        });
    cy.get('#id_password1').type(PASSWORD);
    cy.get('#id_password2').type(PASSWORD);
    for (const _ of waitingFor('POST',
        '/registration/password/reset/confirm/')) {
      cy.get('#id_submit').click();
    }
    cy.contains($t('msgPasswordChanged'));
  });

  it('redirects to login page when visiting gym map while logged out',
      () => {
        cy.visit(`gym-map/${GYM_NAME}`);
        cy.contains($t('notLoggedInMsg'));
      });
});
describe('The register app', () => {
  beforeEach(() => {
    cy.visit('register');
  });

  it('allows registering, logging in, and deleting one\'s account ' +
    'afterwards', () => {
    cy.log('register');
    cy.get('#id_username')
        .type(NEW_USERNAME)
        .should('have.value', NEW_USERNAME);
    cy.get('#id_email')
        .type(NEW_EMAIL)
        .should('have.value', NEW_EMAIL);
    cy.get('#id_password1').type(NEW_PASSWORD);
    cy.get('#id_password2').type(NEW_PASSWORD);
    for (const _ of waitingFor('POST', '/registration/')) {
      cy.get('#submit_button').click();
    }
    cy.contains($t('msgConfirmationEmailSent', {email: NEW_EMAIL}));

    cy.log('confirm email via confirmation link sent via email');
    cy.task('readLastEmail')
        .should('have.string', NEW_EMAIL.toLowerCase())
        .then((mail) => {
          const confirmationLink = /(https?:\/\/[^\s]+)/g
              .exec(mail)[0]
              .replace('localhost:8000', 'localhost:8080');
          cy.visit(confirmationLink);
        });
    for (const _ of waitingFor('POST', '/registration/verify-email/')) {
      cy.get('#id_confirm_email').click();
    }
    cy.contains($t('msgEmailConfirmed'));
    cy.get('#id_alert-0 > .v-alert__close').click();
    cy.contains($t('msgEmailConfirmed')).should('not.exist');


    cy.log('login with newly created credentials');
    cy.visit('login');
    loginViaLogInLink(NEW_EMAIL, NEW_PASSWORD);

    cy.log('check that user is logged in');
    cy.visit('profile');
    cy.contains($t('welcomeMsg', {user: NEW_USERNAME}));

    cy.log('delete account');
    for (const _ of waitingFor('DELETE', '/registration/user/3/')) {
      cy.contains('Delete Account').click();
    }

    cy.log('check that logging in with deleted account leads to error message');
    loginViaLogInLink(NEW_EMAIL, NEW_PASSWORD);
    cy.contains($t('wrongCredentialsMsg'));
  });

  it('shows errors when fields are empty', () => {
    cy.get('#submit_button').click();
    [
      'lblUsername',
      'lblConfirmPassword',
      'lblPassword',
      'lblEmail',
    ].forEach((key) => {
      cy.contains($t('msgRequiredField', {field: $t(key)}));
    });
  });

  it('shows an error for invalid emails', () => {
    cy.get('#id_email').type('thisIsNotAnEmail');
    cy.get('#submit_button').click();
    cy.contains($t('msgInvalidEmail'));
  });

  it('shows an error when passwords do not match', () => {
    cy.get('#id_password1').type('password1');
    cy.get('#id_password2').type('password2');
    cy.get('#submit_button').click();
    cy.contains($t('msgPasswordsDoNotMatch'));
  });

  it('shows an error when passwords are too short', () => {
    cy.get('#id_password1').type('passwor');
    cy.get('#id_password2').type('passwor');
    cy.get('#submit_button').click();
    cy.contains($t('msgPasswordTooShort'));
  });

  it('shows an error when passwords are numeric', () => {
    cy.get('#id_password1').type('12345678');
    cy.get('#id_password2').type('12345678');
    cy.get('#submit_button').click();
    cy.contains($t('msgNumericPassword'));
  });

  it('shows an error when password resembles user name', () => {
    cy.get('#id_username').type(NEW_USERNAME);
    cy.get('#id_email').type(NEW_EMAIL);
    cy.get('#id_password1').type(NEW_USERNAME);
    cy.get('#id_password2').type(NEW_USERNAME);
    for (const _ of waitingFor('POST', '/registration/')) {
      cy.get('#submit_button').click();
    }
    cy.contains('The password is too similar to the username.');
  });

  it('shows an error for common passwords', () => {
    cy.get('#id_username').type(NEW_USERNAME);
    cy.get('#id_email').type(NEW_EMAIL);
    cy.get('#id_password1').type('bigpimpin1');
    cy.get('#id_password2').type('bigpimpin1');
    for (const _ of waitingFor('POST', '/registration/')) {
      cy.get('#submit_button').click();
    }
    cy.contains('This password is too common.');
  });
});

describe('The password change view', () => {
  beforeEach(() => {
    cy.visit('registration/password/reset/change/0/0');
  });

  it('shows an error when passwords do not match', () => {
    cy.get('#id_password1').type('password1');
    cy.get('#id_password2').type('password2');
    cy.get('#id_submit').click();
    cy.contains($t('msgPasswordsDoNotMatch'));
  });
});

describe('The app drawer', () => {
  beforeEach(() => {
    cy.visit('login');
    cy.get('.mdi-menu').click();
  });

  it.only('allows opening the privacy policy page', () => {
    cy.contains($t('appView.privacyPolicy')).click();
    cy.contains($t('privacyPolicy.introduction'));
  });
});
