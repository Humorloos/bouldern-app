describe('The register app', () => {
  it('notifys correctly if user does not exist', () => {
    // try log in with non-existent user
    cy.visit(`${Cypress.env('host')}/bouldern`);

    cy.verifyLogInWithInvalidUser();
  });

  it('lets users log in once they have signed up', () => {
    // Sign up
    cy.visit(`${Cypress.env('host')}/registration/signup`);

    cy.get('#id_username')
        .type(Cypress.env('username'))
        .should('have.value', Cypress.env('username'));
    cy.get('#id_email')
        .type(Cypress.env('email'))
        .should('have.value', Cypress.env('email'));
    cy.get('#id_password1').type(Cypress.env('password'));
    cy.get('#id_password2').type(Cypress.env('password'));
    cy.get('#submit_button').contains('Sign Up').click();

    // Log in after signing up
    cy.enterCredentialsAndLogin();
  });
  it('lets users log out and log in again', () => {
    // Sign out
    cy.contains('Log Out').click();

    cy.logInViaLogInLink();
    cy.contains('You\'re at the bouldern index');
  });
  it('lets users delete their account', () => {
    cy.get('#delete_account').click();
    cy.verifyLogInWithInvalidUser();
  });
});
