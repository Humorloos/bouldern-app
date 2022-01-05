describe('The color creation view', () => {
  it('allows adding colors', () => {
    cy.visit(`${constants.hostVue}/login`);
    loginViaLogInLink(constants.email, constants.password);
    cy.contains('Home').click();
    cy.contains('Create Color').click();
    cy.get('#id_name').type(constants.colorName);
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
    cy.contains('Create Gym').click();
    cy.get('#id_color-level-1').click();
    // newly created color should be in selectable
    cy.contains(constants.colorName).click();
  });
});
