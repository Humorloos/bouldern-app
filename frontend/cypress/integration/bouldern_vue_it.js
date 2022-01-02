describe('The bouldern app', () => {
  it('allows adding gyms', () => {
    cy.visit(`${Cypress.env('hostVue')}/`);
    cy.registerAndLoginVue();
    cy.contains('Create Gym').click();
    cy.get('#id_name').type(Cypress.env('gymName'));
    cy.get('#id_map').attachFile('generic_gym.png');
    cy.contains('Submit').click();
  });
  it('allows adding colors', () => {
    cy.contains('Create Color').click();
    cy.get('#id_name').type(Cypress.env('colorName'));
    cy.get('#id_color').click();
    cy.get('div[style=' +
          '"background: rgba(255, 0, 0, 0.2); ' +
          'opacity: 0; position: absolute; ' +
          'left: 0px; top: 0px; ' +
          'width: 201px; ' +
          'height: 127px; ' +
          'cursor: crosshair;"]')
        .click(150, 50);
    cy.get('#submit_button').click();
  });
});