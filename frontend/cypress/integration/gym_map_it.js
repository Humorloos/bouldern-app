describe('The bouldern app', () => {
  it('lets users add new colors', () => {
    // add gym
    cy.registerAndLogin();
    cy.visit(`${Cypress.env('host')}/bouldern/add-gym/`);
    cy.contains('New Color').click();
    cy.get('div.jquery-modal #id_name').type(Cypress.env('colorName'));
    cy.get('#id_color').click();
    cy.get('div[style="' +
        'background: rgba(255, 0, 0, 0.2); ' +
        'opacity: 0; ' +
        'position: absolute; ' +
        'left: 0px; top: 0px; ' +
        'width: 245px; ' +
        'height: 176px; ' +
        'cursor: crosshair;"]')
        .click(150, 50);
    cy.get('div.jquery-modal #submit_button').click();

    cy.get('#difficulty-level').click();
    cy.contains(Cypress.env('colorName')).click();
  });
  it('lets users create new gyms', () => {
    cy.get('#id_name').type(Cypress.env('newGymName'));
    cy.get('#id_map').attachFile('generic_gym.png');
    cy.contains('Add Level').click();
    cy.get('#difficulty-level:nth-of-type(2)').click();
    cy.contains('Yellow').click();
    cy.contains('Submit').click();
    cy.contains(`Hello, ${Cypress.env('newUsername')}. ` +
        `You're at the bouldern index.`);
  });
  it('can add boulders to gyms', () => {
    cy.visit(
        `${Cypress.env('host')}/bouldern/${Cypress.env('newGymName')}/map/`);
    cy.get('#map-root').click(340, 150);
    cy.contains('You clicked here');
    cy.get('#popup-closer').click();
    cy.get('#map-root').click(340, 210);
    cy.contains('Submit').click();
    cy.get('#id_boulder-0-coordinates')
        .should('have.attr', 'value')
        .then(((value) => {
          value = JSON.parse(value);
          expect(value).to.have.keys('type', 'coordinates');
          expect(value.type).to.eq('Point');
        }));
  });
});
