describe('The gym map view', () => {
  it('allows adding boulders', () => {
    cy.visit(`${Cypress.env('hostVue')}/login`);
    cy.logInViaLogInLink();
    cy.contains(`Hello, ${Cypress.env('email')}. ` +
          'You\'re at the bouldern index.');
    cy.contains('Home').click();
    cy.get('#id_gym-name').type(Cypress.env('gymName'));
    cy.get('#submit_button').click();
    cy.wait(500);
    cy.get('#map-root').click(340, 150);
    cy.contains('You clicked here');
    cy.get('#popup-closer').click();
    cy.get('#map-root').click(340, 210);
    cy.contains('Submit').click();
    cy.contains('Home').click();
  });
});
