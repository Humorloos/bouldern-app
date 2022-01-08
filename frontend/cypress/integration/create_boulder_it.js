describe('The gym map view', () => {
  it('allows adding boulders', () => {
    cy.visit('login');
    loginViaLogInLink(constants.email, constants.password);
    cy.contains(`Hello, ${constants.email}. ` +
      'You\'re at the bouldern index.');
    cy.contains('Home').click();
    cy.get('#id_gym-name').type(constants.gymName);
    cy.get('#submit_button').click();
    // todo: instead import gymmapview and use gymmapview.name, but this needs
    //  webpackconfig of cypress to be same as that of vue
    cy.window()
        .its('GymMapView.$data.loaded').should('equal', true);
    cy.get('#map-root').click(340, 150);
    cy.contains('You clicked here');
    cy.get('#popup-closer').click();
    cy.get('#map-root').click(340, 210);
    cy.contains('Submit').click();
    cy.contains('Home').click();
  });
});
