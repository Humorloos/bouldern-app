describe('The gym creation view', () => {
  it('allows adding gyms', () => {
    cy.visit(`${Cypress.env('hostVue')}/`);
    cy.contains('Log In').click();
    // log in with registered user
    cy.logInViaLogInLinkVue();
    cy.contains(`Hello, ${Cypress.env('email')}. ` +
          'You\'re at the bouldern index.');
    cy.contains('Home').click();
    cy.contains('Create Gym').click();
    cy.get('#id_name').type(Cypress.env('newGymName'));
    cy.get('#id_map').attachFile('generic_gym.png');
    cy.get('#id_color-level-1').click();
    cy.contains('Blue').click();
    cy.contains('Add Level').click();
    cy.get('#id_color-level-2').click();
    cy.contains('Yellow').click();
    cy.contains('Submit').click();
    cy.openNewGymMap();
  });
});
