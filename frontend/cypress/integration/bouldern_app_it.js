/** @file bouldern app tests */

import {
  BOULDER_1_COORDINATES,
  BOULDER_2_COORDINATES,
  COLOR_NAME,
  GREEN_GYM_NAME,
  GYM_NAME,
  NEW_BOULDER_2_COORDINATES,
  NEW_BOULDER_COORDINATES,
  NEW_GYM_NAME,
} from '../support/constants.js';
import {
  atGymMapCoordinates,
  moveBoulder,
  waitForGymMap,
  waitingFor,
} from '../support/functions.js';

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
  beforeEach(() => {
    cy.visit('create-color');
  });

  it('shows an error when name is missing', () => {
    cy.get('.v-col > #submit_button').click();
    cy.contains($t('msgRequiredField', {field: $t('lblName')}));
  });

  it('allows adding colors', () => {
    cy.log('fill in form');
    cy.get('#id_name').type(COLOR_NAME);
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

    cy.log('submit form');
    for (const _ of waitingFor('POST', '/bouldern/color')) {
      cy.get('.v-col > #submit_button').click();
    }

    cy.log('verify that created color can be selected when creating a new gym');
    cy.visit('create-gym');
    cy.get('#id_color-grade-1').click();
    cy.log('newly created color should be in selectable');
    cy.contains(COLOR_NAME).click();
  });
});

describe('The boulder holder', () => {
  it('loads the last opened gym at root', () => {
    for (const _ of waitingFor(
        'GET', `/bouldern/gym-map-resources/?name=${GREEN_GYM_NAME}`)) {
      cy.visit(`gym-map/${GREEN_GYM_NAME}`);
      cy.visit('');
    }
    for (const _ of waitingFor(
        'GET', `/bouldern/gym-map-resources/?name=${GYM_NAME}`)) {
      cy.visit(`gym-map/${GYM_NAME}`);
    }
    cy.get('#id_home').click();
    waitForGymMap();
  });
});

describe('The gym map view', () => {
  beforeEach(() => {
    cy.visit(`gym-map/${GYM_NAME}`);
    waitForGymMap();
  });

  it('allows adding, editing, and retiring boulders', () => {
    atGymMapCoordinates(NEW_BOULDER_COORDINATES, ([x, y]) => {
      cy.log('open create popover and close it');
      cy.get('#map-root').click(x, y);
      cy.contains('Grade');
      cy.get('#popup-closer').click();
    });
    atGymMapCoordinates(NEW_BOULDER_COORDINATES, ([x, y]) => {
      cy.log('open create popover and submit it');
      cy.get('#map-root').click(x, y);
      cy.get('#id-grade-select').click();
      cy.contains('5').click();
      cy.get('#id-color-select').click();
      cy.contains('Yellow').click();
      cy.contains('Save').click();
    });

    cy.log('open edit popover and close it');
    atGymMapCoordinates(NEW_BOULDER_COORDINATES, ([x, y]) => {
      cy.get('#map-root').click(x, y);
      cy.contains('Added 0 day(s) ago');
      cy.contains($t('ascentResults[0]')).click();
      cy.get('#popup-closer').click();
    });

    cy.log('open edit popover, edit and submit');
    atGymMapCoordinates(NEW_BOULDER_COORDINATES, ([x, y]) => {
      cy.get('#map-root').click(x, y);
      cy.contains($t('ascentResults[0]')).click();
      cy.get('#save-boulder').click();
    });

    cy.log('open edit popover and retire boulder');
    atGymMapCoordinates(NEW_BOULDER_COORDINATES, ([x, y]) => {
      cy.get('#map-root').click(x, y);
      cy.get('#retire-boulder').click();
    });
  });

  it('allows filtering by grade', () => {
    atGymMapCoordinates(BOULDER_1_COORDINATES, ([x, y]) => {
      cy.log('check that boulder is clickable before filtering');
      cy.get('#map-root').click(x, y);
      cy.contains($t('ascentResults[0]'));
      cy.get('#popup-closer').click();
    });

    cy.log('activate filter');
    cy.get('#filter').click();
    cy.contains('1').click();
    cy.get('#close-filter').click();

    cy.log('check that boulder is not clickable');
    atGymMapCoordinates(BOULDER_1_COORDINATES, ([x, y]) => {
      cy.get('#map-root').click(x, y);
      cy.contains('Grade');
      cy.get('#popup-closer').click();
    });

    cy.log('deactivate filter and check that boulder is clickable again');
    cy.get('#filter').click();
    cy.contains('1').click();
    cy.get('#close-filter').click();

    atGymMapCoordinates(BOULDER_1_COORDINATES, ([x, y]) => {
      cy.get('#map-root').click(x, y);
      cy.contains($t('ascentResults[0]'));
      cy.get('#popup-closer').click();
    });
  });

  it('allows moving boulders', () => {
    moveBoulder(BOULDER_1_COORDINATES, NEW_BOULDER_COORDINATES);
    moveBoulder(NEW_BOULDER_COORDINATES, BOULDER_1_COORDINATES);
  });

  it('keeps newly created boulders when changing filter', () => {
    const grade = '2';

    cy.log('create new boulder');
    atGymMapCoordinates(NEW_BOULDER_2_COORDINATES, ([x, y]) => {
      cy.get('#map-root').click(x, y);
      cy.get('#id-grade-select').click();
      cy.contains(grade).click();
      cy.contains('Save').click();
    });

    cy.log('activate filter');
    cy.get('#filter').click();
    cy.contains('all').click();
    cy.contains(grade).click();
    cy.get('#close-filter').click();

    cy.log('open edit popover and retire boulder');
    atGymMapCoordinates(NEW_BOULDER_2_COORDINATES, ([x, y]) => {
      cy.get('#map-root').click(x, y);
      cy.get('#retire-boulder').click();
    });
  });

  it('allows adding and removing favorite gyms', () => {
    cy.log('by default, menu should show favorite');
    cy.get('.mdi-menu').click();
    cy.contains(GYM_NAME);

    cy.log('after disabling favorite, menu should not show favorite anymore');
    cy.get('.mdi-menu').click();
    cy.get('#id_favorite').click();

    cy.get('.mdi-menu').click();
    cy.contains(GYM_NAME).should('not.exist');

    cy.log('after enabling favorite again, menu should show it again');
    cy.get('.mdi-menu').click();
    cy.get('#id_favorite').click();

    cy.get('.mdi-menu').click();
    cy.contains(GYM_NAME);
  });

  it('allows editing grades', () => {
    cy.log('open edit view');
    cy.get('#id_edit_gym').click();

    cy.log('change grade');
    cy.get('#id_color-grade-1').click();
    cy.contains('Blue').click();

    cy.log('add grade');
    cy.contains('Add Grade').click();
    cy.get('#id_color-grade-8').click();
    cy.contains('Grey').click();

    cy.log('remove grade');
    cy.get('#id_remove-grade-4').click();

    cy.log('deactivate undefined grade');
    cy.get('#id_undefined_grade_active').click();

    cy.log('save');
    cy.get('#id_save-gym').click();

    cy.log('open edit view again');
    cy.get('#id_edit_gym').click();

    cy.log('activate undefined grade again');
    cy.get('#id_undefined_grade_active').click();
    cy.get('#id_color-undefined').click();
    cy.contains('Black').click();

    cy.log('save');
    cy.get('#id_save-gym').click();
  });

  it('can refresh', () => {
    cy.log('click refresh button');
    cy.get('.mdi-menu').click();
    cy.get('#id_refresh').click();
  });

  it('keeps filters after refresh', () => {
    cy.log('activate filter');
    cy.get('#filter').click();
    cy.contains('all').click();
    cy.contains('1').click();
    cy.get('.mdi-checkbox-marked + input[value="1"]');
    cy.get('.mdi-checkbox-blank-outline + input[value="2"]');
    cy.get('#close-filter').click();

    cy.log('click refresh button');
    cy.get('.mdi-menu').click();
    cy.get('#id_refresh').click();

    cy.log('check that filter is still the same');
    cy.get('#filter').click();
    cy.get('.mdi-checkbox-marked + input[value="1"]');
    cy.log('checkbox for grade 2 should remain unchecked');
    cy.get('.mdi-checkbox-blank-outline + input[value="2"]');
    cy.get('#close-filter').click();

    cy.log('check that boulder is not clickable');
    atGymMapCoordinates(BOULDER_2_COORDINATES, ([x, y]) => {
      cy.get('#map-root').click(x, y);
      cy.contains('Grade');
      cy.get('#popup-closer').click();
    });
  });
});

describe('The gym creation view', () => {
  beforeEach(() => {
    cy.visit('create-gym');
  });

  it('allows adding gyms', () => {
    cy.log('set name and map');
    cy.get('#id_name').type(NEW_GYM_NAME);
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
      cy.get('#id_save-gym').click();
    }

    cy.log('open newly created gym');
    cy.visit(`gym-map/${NEW_GYM_NAME}`);
    waitForGymMap();

    cy.log('open create popover in newly created gym and submit it');
    atGymMapCoordinates(NEW_BOULDER_2_COORDINATES, ([x, y]) => {
      cy.get('#map-root').click(x, y);
      cy.get('#id-grade-select').click();
      cy.contains('2').click();
      cy.get('#id-color-select').click();
      cy.contains('Red').click();
      cy.contains('Save').click();
    });

    cy.log('open edit popover and retire boulder');
    atGymMapCoordinates(NEW_BOULDER_2_COORDINATES, ([x, y]) => {
      cy.get('#map-root').click(x, y);
      cy.get('#retire-boulder').click();
    });
  });

  it('allows navigating to color creation view', () => {
    cy.contains('New Color').click();
    cy.get('#id_color');
  });

  it('shows errors for empty fields', () => {
    cy.get('#id_save-gym').click();
    ['lblName', 'lblMap'].forEach((key) => {
      cy.contains($t('msgRequiredField', {field: $t(key)}));
    });
  });

  it('shows an error when grades are missing', () => {
    cy.get('#id_remove-grade-1').click();
    cy.get('#id_save-gym').click();
    cy.contains($t('msgNoGrades'));
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
    cy.get('#id_gym-name').type(GYM_NAME);
    cy.get('#submit_button').click();
    waitForGymMap();
  });

  it('allows navigating to favorite gyms', () => {
    cy.contains(GYM_NAME).click();
    waitForGymMap();
  });
});
