describe('The gym map view', () => {
  it('allows adding boulders', () => {
    cy.visit(`${Cypress.env('hostVue')}/`);
    cy.contains('Log In').click();
    // todo: this should not work, but it does, so we need to fix it and
    //  probably won't need the command anymore
    cy.logInViaLogInLink();
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
