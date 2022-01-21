/** @file bouldern app tests */

import GymMapView from '../../src/views/GymMap.vue';

beforeEach(() => {
  cy.visit('', {
    onLoad: (win) => {
      win.$store.dispatch('setLoginData', cy.loginData);
    },
  });
  cy.window().its('$store.state.authToken.token').should('not.be.empty');
});

describe('The color creation view', () => {
  it('allows adding colors', () => {
    cy.visit('create-color');
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
    cy.get('.v-main__wrap').click();
    cy.intercept('POST', '/bouldern/color').as('createColor');
    cy.get('.v-form > #submit_button').click();
    cy.wait('@createColor');
    cy.visit('create-gym');
    cy.get('#id_color-level-1').click();
    // newly created color should be in selectable
    cy.contains(constants.colorName).click();
  });
});


describe('The gym map view', () => {
  it('allows adding boulders', () => {
    cy.get('#id_gym-name').type(constants.gymName);
    cy.get('#submit_button').click();
    cy.window().its(`${GymMapView.name}.$data.loaded`).should('equal', true);
    cy.get('#map-root').click(140, 270);
    cy.contains('You clicked here');
    cy.get('.ol-popup-closer').click();
    cy.get('#map-root').click(340, 210);
    cy.contains('Submit').click();
    cy.contains('Home').click();
  });
});

describe('The gym creation view', () => {
  it('allows adding gyms', () => {
    cy.contains('Create Gym').click();
    cy.get('#id_name').type(constants.newGymName);
    cy.get('#id_map').attachFile('generic_gym.png');
    cy.get('#id_color-level-1').click();
    cy.contains('Blue').click();
    cy.contains('Add Level').click();
    cy.get('#id_color-level-2').click();
    cy.contains('Yellow').click();
    cy.contains('Submit').click();
    cy.get('#id_gym-name').type(constants.newGymName);
    cy.get('#submit_button').click();
  });
});
