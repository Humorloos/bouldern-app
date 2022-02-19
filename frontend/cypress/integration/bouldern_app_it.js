/** @file bouldern app tests */

import GymMapView from '../../src/views/GymMap.vue';

beforeEach(() => {
  cy.visit('login', {
    onLoad: (win) => {
      win.$store.dispatch('setLoginData', cy.loginData);
    },
  });
  cy.window().its('$store.state.authToken.token').should('not.be.empty');
  for (const _ of waitingFor('GET', '/bouldern/favorite-gym')) {
    cy.window().its('$store')
        .then((store) => store.dispatch('loadFavoriteGyms'));
  }
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
    cy.get('#id_color-grade-1').click();
    cy.log('newly created color should be in selectable');
    cy.contains(constants.colorName).click();
  });
});

describe('The gym map view', () => {
  it('allows adding, editing, and retiring boulders', () => {
    cy.visit(`gym-map/${constants.gymName}`);
    cy.window().its(`${GymMapView.name}.loaded`).should('equal', true);

    cy.log('open create popover and close it');
    cy.get('#map-root').click(140, 270);
    cy.contains('Grade');
    cy.get('#popup-closer').click();

    cy.log('open create popover and submit it');
    cy.get('#map-root').click(280, 240);
    cy.get('#id-grade-select').click();
    cy.contains('5').click();
    cy.get('#id-color-select').click();
    cy.contains('Yellow').click();
    cy.contains('Save').click();

    cy.log('open edit popover and close it');
    cy.get('#map-root').click(50, 300);
    // we have to click twice because there is a bug that the popover is not
    // moved correctly the first time
    cy.get('#map-root').click(50, 300);
    cy.contains('Added 0 day(s) ago');
    cy.contains($t('ascentResults[0]')).click();
    cy.get('#popup-closer').click();

    cy.log('open edit popover, edit and submit');
    cy.get('#map-root').click(60, 370);
    cy.contains($t('ascentResults[0]')).click();
    cy.get('#save-boulder').click();

    cy.log('open edit popover and retire boulder');
    cy.get('#map-root').click(50, 370);
    cy.get('#retire-boulder').click();
  });

  it('loads the last opened gym at root', () => {
    for (const _ of waitingFor(
        'GET', `/bouldern/gym-map-resources/?name=${constants.greenGymName}`)) {
      cy.visit(`gym-map/${constants.greenGymName}`);
      cy.visit('');
    }
    for (const _ of waitingFor(
        'GET', `/bouldern/gym-map-resources/?name=${constants.gymName}`)) {
      cy.visit(`gym-map/${constants.gymName}`);
    }
    cy.get('.v-app-bar-title__placeholder').click();
    cy.window().its(`${GymMapView.name}.loaded`).should('equal', true);
  });

  it('allows filtering by grade', () => {
    cy.visit(`gym-map/${constants.gymName}`);
    cy.window().its(`${GymMapView.name}.loaded`).should('equal', true);

    cy.window().its(
        `${GymMapView.name}.$refs.overlay.popover.autoPan.animation.duration`,
    ).then((duration) => {
      cy.wait(duration);
    });

    cy.log('check that boulder is clickable before filtering');
    cy.get('#map-root').click(240, 340);
    cy.contains($t('ascentResults[0]'));
    cy.get('#popup-closer').click();

    cy.log('activate filter and check that boulder is not clickable');
    cy.get('#filter').click();
    cy.contains('1').click();
    cy.get('#close-filter').click();

    cy.get('#map-root').click(50, 370);
    cy.contains('Grade');
    cy.get('#popup-closer').click();

    cy.log('deactivate filter and check that boulder is clickable again');
    cy.get('#filter').click();
    cy.contains('1').click();
    cy.get('#close-filter').click();

    cy.get('#map-root').click(50, 370);
    cy.contains($t('ascentResults[0]'));
    cy.get('#popup-closer').click();
  });

  it('allows adding and removing favorite gyms', () => {
    cy.visit(`gym-map/${constants.gymName}`);

    cy.log('by default, menu should show favorite');
    cy.get('.mdi-menu').click();
    cy.contains(constants.gymName);

    cy.log('after disabling favorite, menu should not show favorite anymore');
    cy.get('.mdi-menu').click();
    cy.get('#id_favorite').click();

    cy.get('.mdi-menu').click();
    cy.contains(constants.gymName).should('not.exist');

    cy.log('after enabling favorite again, menu should show it again');
    cy.get('.mdi-menu').click();
    cy.get('#id_favorite').click();

    cy.get('.mdi-menu').click();
    cy.contains(constants.gymName);
  });
});

describe('The gym creation view', () => {
  beforeEach(() => {
    cy.visit('create-gym');
  });

  it('allows adding gyms', () => {
    cy.get('#id_name').type(constants.newGymName);
    cy.get('#id_map').attachFile('generic_gym.png');
    cy.get('#id_color-grade-1').click();
    cy.contains('Blue').click();
    cy.contains('Add Grade').click();
    cy.get('#id_color-grade-2').click();
    cy.contains('Yellow').click();
    for (const _ of waitingFor('POST', '/bouldern/gym')) {
      cy.contains('Submit').click();
    }
    cy.visit(`gym-map/${constants.newGymName}`);
    cy.window().its(`${GymMapView.name}.loaded`).should('equal', true);
  });

  it('allows navigating to color creation view', () => {
    cy.contains('New Color').click();
    cy.get('#id_color');
  });
});

describe('The home view', () => {
  it('shows the gym search when no gym is active', () => {
    cy.visit('');
    cy.contains('Find Gym');
  });
});

describe('The app drawer', () => {
  beforeEach(() => {
    cy.get('.mdi-menu').click();
  });

  it('allows navigating to gym creation view', () => {
    cy.contains('New Gym').click();
    cy.get('#id_map');
  });

  it('allows navigating to a gym map view', () => {
    cy.get('#id_gym-name').type(constants.gymName);
    cy.get('#submit_button').click();
    cy.window().its(`${GymMapView.name}.loaded`).should('equal', true);
  });

  it('allows navigating to favorite gyms', () => {
    cy.contains(constants.gymName).click();
    cy.window().its(`${GymMapView.name}.loaded`).should('equal', true);
  });
});
