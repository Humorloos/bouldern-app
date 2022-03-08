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
        .then((store) => {
          store.dispatch('loadFavoriteGyms');
          store.dispatch('loadColors');
        });
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
      cy.get('.v-col > #submit_button').click();
    }
    cy.visit('create-gym');
    cy.get('#id_color-grade-1').click();
    cy.log('newly created color should be in selectable');
    cy.contains(constants.colorName).click();
  });
});

describe('The boulder holder', () => {
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
    cy.get('#id_home').click();
    cy.window().its(`${GymMapView.name}.loaded`).should('equal', true);
  });
});

describe('The gym map view', () => {
  beforeEach(() => {
    cy.visit(`gym-map/${constants.gymName}`);
    cy.window().its(`${GymMapView.name}.loaded`).should('equal', true);
  });

  it('allows adding, editing, and retiring boulders', () => {
    cy.window().its(`${GymMapView.name}.map`).then((map) => {
      atPixel(map, constants.newBoulderCoordinates, ([x, y]) => {
        cy.log('open create popover and close it');
        cy.get('#map-root').click(x, y);
        cy.contains('Grade');
        cy.get('#popup-closer').click();
      });
      atPixel(map, constants.newBoulderCoordinates, ([x, y]) => {
        cy.log('open create popover and submit it');
        cy.get('#map-root').click(x, y);
        cy.get('#id-grade-select').click();
        cy.contains('5').click();
        cy.get('#id-color-select').click();
        cy.contains('Yellow').click();
        cy.contains('Save').click();
      });
      atPixel(map, constants.newBoulderCoordinates, ([x, y]) => {
        cy.log('open edit popover and close it');
        cy.get('#map-root').click(x, y);
        // we have to click twice because there is a bug that the popover is not
        // moved correctly the first time
        // cy.get('#map-root').click(x, y);
        cy.contains('Added 0 day(s) ago');
        cy.contains($t('ascentResults[0]')).click();
        cy.get('#popup-closer').click();
      });
      atPixel(map, constants.newBoulderCoordinates, ([x, y]) => {
        cy.log('open edit popover, edit and submit');
        cy.get('#map-root').click(x, y);
        cy.contains($t('ascentResults[0]')).click();
        cy.get('#save-boulder').click();
      });
      atPixel(map, constants.newBoulderCoordinates, ([x, y]) => {
        cy.log('open edit popover and retire boulder');
        cy.get('#map-root').click(x, y);
        cy.get('#retire-boulder').click();
      });
    });
  });

  it('allows filtering by grade', () => {
    cy.window().its(`${GymMapView.name}.map`).then((map) => {
      atPixel(map, constants.boulder1Coordinates, ([x, y]) => {
        cy.log('check that boulder is clickable before filtering');
        cy.get('#map-root').click(x, y);
        cy.contains($t('ascentResults[0]'));
        cy.get('#popup-closer').click();
      });

      cy.log('activate filter and check that boulder is not clickable');
      cy.get('#filter').click();
      cy.contains('1').click();
      cy.get('#close-filter').click();

      atPixel(map, constants.boulder1Coordinates, ([x, y]) => {
        cy.get('#map-root').click(x, y);
        cy.contains('Grade');
        cy.get('#popup-closer').click();
      });

      cy.log('deactivate filter and check that boulder is clickable again');
      cy.get('#filter').click();
      cy.contains('1').click();
      cy.get('#close-filter').click();

      atPixel(map, constants.boulder1Coordinates, ([x, y]) => {
        cy.get('#map-root').click(x, y);
        cy.contains($t('ascentResults[0]'));
        cy.get('#popup-closer').click();
      });
    });
  });

  it('allows adding and removing favorite gyms', () => {
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
  it('allows editing grades', () => {
    // open edit view
    cy.get('#id_edit_gym').click();

    // change grade
    cy.get('#id_color-grade-1').click();
    cy.contains('Blue').click();

    // add grade
    cy.contains('Add Grade').click();
    cy.get('#id_color-grade-8').click();
    cy.contains('Grey').click();

    // remove grade
    cy.get('#id_remove-grade-4').click();

    // deactivate undefined grade
    cy.get('#id_undefined_grade_active').click();

    // save
    cy.get('#id_save-gym').click();

    // open edit view again
    cy.get('#id_edit_gym').click();

    // activate undefined grade again
    cy.get('#id_undefined_grade_active').click();
    cy.get('#id_color-undefined').click();
    cy.contains('Black').click();

    // save
    cy.get('#id_save-gym').click();
  });

  it('can refresh', () => {
    cy.log('click refresh button');
    cy.get('.mdi-menu').click();
    cy.get('#id_refresh').click();
  });
});

describe('The gym creation view', () => {
  beforeEach(() => {
    cy.visit('create-gym');
  });

  it('allows adding gyms', () => {
    cy.log('set name and map');
    cy.get('#id_name').type(constants.newGymName);
    cy.get('#id_map').attachFile('generic_gym.png');

    cy.log('set grades');
    cy.get('#id_color-grade-1').click();
    cy.contains('Blue').click();
    cy.contains('Add Grade').click();
    cy.get('#id_color-grade-2').click();
    cy.contains('Yellow').click();

    cy.log('set undefined grade');
    cy.get('#id_undefined_grade_active').click();
    cy.get('#id_color-undefined').click();
    cy.contains('Grey').click();

    cy.log('submit');
    for (const _ of waitingFor('POST', '/bouldern/gym')) {
      cy.contains('Submit').click();
    }

    cy.log('open newly created gym');
    cy.visit(`gym-map/${constants.newGymName}`);
    cy.window().its(`${GymMapView.name}.loaded`).should('equal', true);

    cy.log('open create popover in newly created gym and submit it');
    cy.get('#map-root').click(280, 240);
    cy.get('#id-grade-select').click();
    cy.contains('2').click();
    cy.get('#id-color-select').click();
    cy.contains('Red').click();
    cy.contains('Save').click();
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
