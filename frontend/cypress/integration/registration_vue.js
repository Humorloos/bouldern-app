describe('The register vue app', () => {
  it('notifys correctly if user does not exist', () => {
    // try log in with non-existent user
    cy.visit(`${Cypress.env('hostVue')}/login`);
    cy.logInViaLogInLinkVue();
    cy.contains('Please enter a correct email and password.');
  });

  it('allows registering', () => {
    cy.visit(`${Cypress.env('hostVue')}/register`);

    cy.register();
  });
});
