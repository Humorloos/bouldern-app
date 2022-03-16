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

  it('allows registering again after deleting one\'s account', () => {
    cy.log('delete account');
    cy.visit('profile');
    for (const _ of waitingFor('DELETE', '/registration/user/2/')) {
      cy.contains('Delete Account').click();
    }

    cy.log('check that logging in with deleted account leads to error message');
    loginViaLogInLink(constants.email, constants.password);
    cy.contains($t('wrongCredentialsMsg'));

    cy.log('register');
    cy.visit('register');
    cy.get('#id_username').type(constants.username);
    cy.get('#id_email').type(constants.email);
    cy.get('#id_password1').type(constants.password);
    cy.get('#id_password2').type(constants.password);
    for (const _ of waitingFor('POST', '/registration/')) {
      cy.get('#submit_button').click();
    }
    cy.contains($t('confirmationEmailAlert', {email: constants.email}));

    cy.log('confirm email via confirmation link sent via email');
    cy.task('readLastEmail')
        .should('have.string', constants.email.toLowerCase())
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
    loginViaLogInLink(constants.email, constants.password);

    cy.log('check that user is logged in');
    cy.visit('profile');
    cy.contains($t('welcomeMsg', {user: constants.username}));
  });
});

describe('The login view', () => {
  beforeEach(() => {
    cy.visit('login');
  });

  it('shows an error message when trying to log in with wrong crendentials',
      () => {
        // try log in with non-existent user
        loginViaLogInLink(constants.newEmail, constants.newPassword);
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

  it('redirects to login page when visiting gym map while logged out',
      () => {
        cy.visit(`gym-map/${constants.gymName}`);
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

    cy.log('confirm email via confirmation link sent via email');
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

    cy.log('login with newly created credentials');
    cy.visit('login');
    loginViaLogInLink(constants.newEmail, constants.newPassword);

    cy.log('check that user is logged in');
    cy.visit('profile');
    cy.contains($t('welcomeMsg', {user: constants.newUsername}));

    cy.log('delete account');
    for (const _ of waitingFor('DELETE', '/registration/user/3/')) {
      cy.contains('Delete Account').click();
    }

    cy.log('check that logging in with deleted account leads to error message');
    loginViaLogInLink(constants.newEmail, constants.newPassword);
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
    cy.get('#id_username').type(constants.newUsername);
    cy.get('#id_email').type(constants.newEmail);
    cy.get('#id_password1').type(constants.newUsername);
    cy.get('#id_password2').type(constants.newUsername);
    for (const _ of waitingFor('POST', '/registration/')) {
      cy.get('#submit_button').click();
    }
    cy.contains('The password is too similar to the username.');
  });

  it('shows an error for common passwords', () => {
    cy.get('#id_username').type(constants.newUsername);
    cy.get('#id_email').type(constants.newEmail);
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
