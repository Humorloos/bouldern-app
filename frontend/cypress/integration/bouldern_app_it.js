/** @file bouldern app tests */

import GymMapView from '../../src/views/GymMap.vue';

beforeEach(() => {
  cy.visit('login', {
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
    for (const _ of waitingFor('POST', '/bouldern/color')) {
      cy.get('.v-form > #submit_button').click();
    }
    cy.visit('create-gym');
    cy.get('#id_color-level-1').click();
    // newly created color should be in selectable
    cy.contains(constants.colorName).click();
  });
});


describe('The gym map view', () => {
  it('allows adding boulders', () => {
    cy.visit('');
    cy.window().its(`${GymMapView.name}.$data.loaded`).should('equal', true);
    cy.get('#map-root').click(140, 270);
    cy.contains('Difficulty');
    cy.get('#popup-closer').click();
    cy.get('#map-root').click(280, 240);
    cy.get('#id-difficulty-select').click();
    cy.contains('5').click();
    cy.get('#id-color-select').click();
    cy.contains('Yellow').click();
    cy.contains('Save').click();
  });

  it('loads the last opened gym at root', () => {
    for (const _ of waitingFor(
        'GET', `/bouldern/gym/?name=${constants.greenGymName}`)) {
      cy.visit(`gym-map/${constants.greenGymName}`);
      cy.visit('');
    }
    for (const _ of waitingFor(
        'GET', `/bouldern/gym/?name=${constants.gymName}`)) {
      cy.visit(`gym-map/${constants.gymName}`);
    }
    cy.get('.v-app-bar-title__placeholder').click();
    cy.window().its(`${GymMapView.name}.$data.loaded`).should('equal', true);
  });

  it('shows the edit popup when clicking a boulder', () => {
    cy.visit('');
    cy.window().its(`${GymMapView.name}.$data.loaded`).should('equal', true);
    cy.window().its(
        `${GymMapView.name}.$refs.overlay.popover.autoPan.animation.duration`,
    ).then((duration) => {
      cy.wait(duration);
    });
    cy.get('#map-root').click(240, 340);
    cy.contains($t('ascendResults[0]')).click();
    cy.get('#popup-closer').click();
    cy.get('#map-root').click(50, 370);
    cy.contains($t('ascendResults[0]')).click();
    cy.get('#save-boulder').click();
    cy.get('#map-root').click(50, 370);
    cy.get('#retire-boulder').click();
  });
});

describe('The gym creation view', () => {
  it('allows adding gyms', () => {
    cy.visit('create-gym');
    cy.get('#id_name').type(constants.newGymName);
    cy.get('#id_map').attachFile('generic_gym.png');
    cy.get('#id_color-level-1').click();
    cy.contains('Blue').click();
    cy.contains('Add Level').click();
    cy.get('#id_color-level-2').click();
    cy.contains('Yellow').click();
    for (const _ of waitingFor('POST', '/bouldern/gym')) {
      cy.contains('Submit').click();
    }
    cy.visit(`gym-map/${constants.newGymName}`);
    cy.window().its(`${GymMapView.name}.$data.loaded`).should('equal', true);
  });
});

describe('The app drawer', () => {
  beforeEach(() => {
    cy.get('.mdi-menu').click();
  });

  it('allows navigating to color creation view', () => {
    cy.contains('Create Color').click();
    cy.get('#id_color');
  });

  it('allows navigating to gym creation view', () => {
    cy.contains('Create Gym').click();
    cy.get('#id_map');
  });

  it('allows navigating to a gym map view', () => {
    cy.get('#id_gym-name').type(constants.gymName);
    cy.get('#submit_button').click();
    cy.window().its(`${GymMapView.name}.$data.loaded`).should('equal', true);
  });
});
