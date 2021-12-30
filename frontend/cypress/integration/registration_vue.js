describe('The register vue app', () => {
  it('notifys correctly if user does not exist', () => {
    cy.visit(`${Cypress.env('hostVue')}/`);
    cy.contains('Log In').click();

    // try log in with non-existent user
    cy.logInViaLogInLinkVue();
    cy.contains('Please enter a correct email and password.');
    cy.contains('Home').click();
  });

  it('allows logging in after registering', () => {
    cy.registerAndLoginVue();
  });
});
