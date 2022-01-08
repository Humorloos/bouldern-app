describe('The gym map view', () => {
  it('allows adding boulders', () => {
    cy.visit('login');
    loginViaLogInLink(constants.email, constants.password);
    cy.contains(`Hello, ${constants.email}. ` +
      'You\'re at the bouldern index.');
    cy.contains('Home').click();
    cy.get('#id_gym-name').type(constants.gymName);
    cy.get('#submit_button').click();
    cy.wait(1000);
    // todo: instead import gymmapview and use gymmapview.name, but this needs
    //  webpackconfig of cypress to be same as that of vue
    cy.window()
        .its('GymMapView')
        .then((app) => {
          debugger;
        });
    cy.get('canvas').click(340, 150);
    cy.contains('You clicked here');
    cy.get('#popup-closer').click();
    cy.get('#map-root').click(340, 210);
    cy.contains('Submit').click();
    cy.contains('Home').click();
  });
});
