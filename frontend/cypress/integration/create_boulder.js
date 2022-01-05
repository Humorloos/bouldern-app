describe('The gym map view', () => {
  it('allows adding boulders', () => {
    cy.visit(`${Cypress.env('hostVue')}/`);
    cy.contains('Log In').click();
    cy.logInViaLogInLinkVue();
    cy.contains(`Hello, ${Cypress.env('email')}. ` +
          'You\'re at the bouldern index.');
    cy.contains('Home').click();
    cy.openGymMap();
    cy.get('#map-root').click(340, 150);
    cy.contains('You clicked here');
    cy.get('#popup-closer').click();
    cy.get('#map-root').click(340, 210);
    cy.contains('Submit').click();
    cy.contains('Home').click();
  });
});
