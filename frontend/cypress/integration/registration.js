describe('The register app', () => {
  it('notifys correctly if user does not exist', () => {
    // try log in with non-existent user
    cy.visit(`${Cypress.env('host')}/bouldern`);

    cy.verifyLogInWithInvalidUser();
  });

  it('lets users log in once they have signed up', () => {
    // Sign up
    cy.registerAndLogin();
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
