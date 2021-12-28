describe('The register vue app', () => {
  it('allows registering', () => {
    cy.visit(`${Cypress.env('hostVue')}/`);

    cy.register();
  });
});
