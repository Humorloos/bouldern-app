describe('The register vue app', () => {
  it('notifys correctly if user does not exist', function() {
    cy.visit(`${constants.hostVue}/`);
    cy.contains('Log In').click();
    // try log in with non-existent user
    cy.logInViaLogInLinkNew();
    cy.contains($t('wrongCredentialsMsg'));
    cy.contains('Home').click();
  });

  it('allows logging in after registering', () => {
    cy.contains('Register').click();

    cy.get('#id_username')
        .type(Cypress.env('newUsername'))
        .should('have.value', Cypress.env('newUsername'));
    cy.get('#id_email')
        .type(Cypress.env('newEmail'))
        .should('have.value', Cypress.env('newEmail'));
    cy.get('#id_password1').type(Cypress.env('newPassword'));
    cy.get('#id_password2').type(Cypress.env('newPassword'));
    cy.get('#submit_button').contains('Register').click();
    cy.contains('Home').click();

    cy.contains('Log In').click();
    cy.logInViaLogInLinkNew();
    cy.contains(`Hello, ${Cypress.env('newEmail')}. ` +
          'You\'re at the bouldern index.');
    cy.contains('Home').click();
  });
  it('allows logging out', () => {
    cy.contains('Log Out').click();
    cy.contains('Log In').click();
    cy.contains($t('notLoggedInMsg'));
  });
  it('allows deleting your account', () => {
    // try log in with non-existent user
    cy.logInViaLogInLink();
    cy.contains('Home').click();
    cy.contains('Delete Account').click();
    cy.contains('Log In').click();
    cy.logInViaLogInLink();
    cy.contains($t('wrongCredentialsMsg'));
  });
});
