/** @file test for registration, login, logout, and account deletion */

after(() => cy.task('log', $log));

describe('The register app', () => {
  it('can register, login, logout, and delete accounts', () => {
    cy.visit('');
    cy.window().then((win) => {
      win.$store.subscribe((mutation, state) => {
        $log[new Date().toISOString() + ' - ' + mutation.type] = {
          mutationPayload: mutation.payload, state: state,
        };
      });
      win.$store.subscribeAction((action, state) => {
        $log[new Date().toISOString() + ' - ' + action.type] = {
          actionPayload: action.payload, state: state,
        };
      });
    });
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
