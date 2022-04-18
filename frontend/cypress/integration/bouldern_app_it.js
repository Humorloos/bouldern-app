/** @file bouldern app tests */

import {
  BOULDER_1_COORDINATES,
  BOULDER_1_GRADE,
  BOULDER_1_HOLD_COLOR,
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
  createBoulder,
  createNewGym,
  getCenter,
  getCurrentCenter,
  login,
  moveBoulder,
  refreshGymMap,
  waitForGymMap,
  waitingFor,
} from '../support/functions.js';
import GymMapView from '../../src/views/GymMap.vue';

beforeEach(() => {
  login();
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

describe('The gym map view', () => {
  beforeEach(() => {
    cy.visit(`gym-map/${GYM_NAME}`);
    waitForGymMap();
  });

  it('allows adding boulders, reporting ascents, and retiring boulders',
      () => {
        atGymMapCoordinates(NEW_BOULDER_COORDINATES, ([x, y]) => {
          cy.log('open create popover and close it');
          cy.get('#id_map-root').click(x, y);
          cy.contains('Grade');
          cy.get('#popup-closer').click();
        }).then(() => {
          cy.log('open create popover and submit it');
          atGymMapCoordinates(NEW_BOULDER_COORDINATES, ([x, y]) => {
            cy.get('#id_map-root').click(x, y);
            cy.get('#id_grade-select').click();
            cy.contains('5').click();
            cy.get('#id_color-select').click();
            cy.contains('Yellow').click();
            cy.contains('Save').click();
          });
        }).then(() => {
          cy.log('open ascent popover and close it');
          atGymMapCoordinates(NEW_BOULDER_COORDINATES, ([x, y]) => {
            cy.get('#id_map-root').click(x, y);
            cy.contains('Added 0 day(s) ago');
            cy.contains($t('gymMap.ascentResults[0]')).click();
            cy.get('#popup-closer').click();
          });
        }).then(() => {
          cy.log('open ascent popover, edit and submit');
          atGymMapCoordinates(NEW_BOULDER_COORDINATES, ([x, y]) => {
            cy.get('#id_map-root').click(x, y);
            cy.contains($t('gymMap.ascentResults[0]')).click();
            cy.get('#save-boulder').click();
          });
        }).then(() => {
          cy.log('open ascent popover and retire boulder');
          atGymMapCoordinates(NEW_BOULDER_COORDINATES, ([x, y]) => {
            cy.get('#id_map-root').click(x, y);
            cy.get('#id_retire-boulder').click();
          });
        });
      });

  it('allows filtering by grade', () => {
    atGymMapCoordinates(BOULDER_1_COORDINATES, ([x, y]) => {
      cy.log('check that boulder is clickable before filtering');
      cy.get('#id_map-root').click(x, y);
      cy.contains($t('gymMap.ascentResults[0]'));
      cy.get('#popup-closer').click();
    });

    cy.log('activate filter');
    cy.get('#id_filter').click();
    cy.contains('1').click();
    cy.get('#close-filter').click();

    cy.log('check that boulder is not clickable');
    atGymMapCoordinates(BOULDER_1_COORDINATES, ([x, y]) => {
      cy.get('#id_map-root').click(x, y);
      cy.contains('Grade');
      cy.get('#popup-closer').click();
    });

    cy.log('deactivate filter and check that boulder is clickable again');
    cy.get('#id_filter').click();
    cy.contains('1').click();
    cy.get('#close-filter').click();

    atGymMapCoordinates(BOULDER_1_COORDINATES, ([x, y]) => {
      cy.get('#id_map-root').click(x, y);
      cy.contains($t('gymMap.ascentResults[0]'));
      cy.get('#popup-closer').click();
    });
  });

  it('allows moving boulders', () => {
    moveBoulder(BOULDER_1_COORDINATES, NEW_BOULDER_COORDINATES);
    moveBoulder(NEW_BOULDER_COORDINATES, BOULDER_1_COORDINATES);
  });

  it('resets a boulder\'s colors when closing the edit popover', () => {
    cy.log('change boulder color and grade and close edit popover');
    atGymMapCoordinates(BOULDER_1_COORDINATES, ([x, y]) => {
      cy.get('#id_map-root').click(x, y);
      cy.get('#id_edit-boulder').click();
      cy.get('#id_grade-select').click().contains('5').click();
      cy.get('#id_color-select').click().contains('Red').click();
      cy.get('#popup-closer').click();
    });
    cy.log('check that boulder\'s color and grade are reset');
    atGymMapCoordinates(BOULDER_1_COORDINATES, ([x, y]) => {
      cy.get('#id_map-root').click(x, y);
      cy.get('#id_edit-boulder').click();
      cy.get('#id_grade-select').contains(BOULDER_1_GRADE);
      cy.get('#id_color-select').contains(BOULDER_1_HOLD_COLOR);
    });
  });

  it('allows editing boulders', () => {
    const NEW_GRADE = '5';
    const NEW_COLOR = 'Red';

    cy.log('change boulder color and grade and save');
    atGymMapCoordinates(BOULDER_1_COORDINATES, ([x, y]) => {
      cy.get('#id_map-root').click(x, y);
      cy.get('#id_edit-boulder').click();
      cy.get('#id_grade-select').click().contains(NEW_GRADE).click();
      cy.get('#id_color-select').click().contains(NEW_COLOR).click();
      cy.get('#id_save-boulder').click();
    });
    cy.log('check boulder\'s color and grade and change back to original' +
      ' values');
    atGymMapCoordinates(BOULDER_1_COORDINATES, ([x, y]) => {
      cy.get('#id_map-root').click(x, y);
      cy.get('#id_edit-boulder').click();
      cy.get('#id_grade-select').contains(NEW_GRADE);
      cy.get('#id_color-select').contains(NEW_COLOR);
      cy.get('#id_grade-select').click().contains(BOULDER_1_GRADE).click();
      cy.get('#id_color-select').click().contains(BOULDER_1_HOLD_COLOR).click();
      cy.get('#id_save-boulder').click();
    });
    cy.log('check boulder\'s color and grade again');
    atGymMapCoordinates(BOULDER_1_COORDINATES, ([x, y]) => {
      cy.get('#id_map-root').click(x, y);
      cy.get('#id_edit-boulder').click();
      cy.get('#id_grade-select').contains(BOULDER_1_GRADE);
      cy.get('#id_color-select').contains(BOULDER_1_HOLD_COLOR);
    });
  });

  it('allows moving newly created boulders after refresh', () => {
    cy.log('create new boulder');
    createBoulder(NEW_BOULDER_2_COORDINATES, '3');

    cy.log('click refresh button');
    refreshGymMap();

    cy.log('move boulder');
    cy.window().its(`${GymMapView.name}`).then((gymMap) => {
      cy.waitUntil(() => {
        return getCurrentCenter(gymMap)[0] === getCenter(gymMap)[0];
      }).then(() => {
        moveBoulder(NEW_BOULDER_2_COORDINATES, NEW_BOULDER_COORDINATES);
      });
    });

    cy.log('open ascent popover and retire boulder');
    atGymMapCoordinates(NEW_BOULDER_COORDINATES, ([x, y]) => {
      cy.get('#id_map-root').click(x, y);
      cy.get('#id_retire-boulder').click();
    });
  });


  it('keeps newly created boulders when changing filter', () => {
    const grade = '2';

    cy.log('create new boulder');
    createBoulder(NEW_BOULDER_2_COORDINATES, grade);

    cy.log('activate filter');
    cy.get('#id_filter').click();
    cy.contains('all').click();
    cy.contains(grade).click();
    cy.get('#close-filter').click();

    cy.log('open ascent popover and retire boulder');
    atGymMapCoordinates(NEW_BOULDER_2_COORDINATES, ([x, y]) => {
      cy.get('#id_map-root').click(x, y);
      cy.get('#id_retire-boulder').click();
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
    cy.get('#id_menu').click();
    cy.contains($t('gymMap.edit')).click();

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
    cy.get('#id_undefined-grade-active').click();

    cy.log('save');
    cy.get('#id_save-gym').click();

    cy.log('open edit view again');
    cy.get('#id_menu').click();
    cy.contains($t('gymMap.edit')).click();

    cy.log('activate undefined grade again');
    cy.get('#id_undefined-grade-active').click();
    cy.get('#id_color-undefined').click();
    cy.contains('Black').click();

    cy.log('save');
    cy.get('#id_save-gym').click();
  });

  it('can refresh', () => {
    cy.log('click refresh button');
    refreshGymMap();
  });

  it('keeps filters after refresh', () => {
    cy.log('activate filter');
    cy.get('#id_filter').click();
    cy.contains('all').click();
    cy.contains('1').click();
    cy.get('.mdi-checkbox-marked + #id_filter-1');
    cy.get('.mdi-checkbox-blank-outline + #id_filter-2');
    cy.get('#close-filter').click();

    cy.log('click refresh button');
    refreshGymMap();

    cy.log('check that filter is still the same');
    cy.get('#id_filter').click();
    cy.get('.mdi-checkbox-marked + #id_filter-1');
    cy.log('checkbox for grade 2 should remain unchecked');
    cy.get('.mdi-checkbox-blank-outline + #id_filter-2');
    cy.get('#close-filter').click();

    cy.log('check that boulder is not clickable');
    atGymMapCoordinates(BOULDER_2_COORDINATES, ([x, y]) => {
      cy.get('#id_map-root').click(x, y);
      cy.contains('Grade');
      cy.get('#popup-closer').click();
    });
  });

  it('resets filters when changing gym', () => {
    cy.log('activate filter');
    cy.get('#id_filter').click();
    cy.contains('all').click();
    cy.contains('1').click();
    cy.get('#close-filter').click();

    cy.log('open green gym');
    cy.visit(`gym-map/${GREEN_GYM_NAME}`);
    waitForGymMap();

    cy.log('check that filters are reset');
    cy.get('#id_filter').click();
    cy.get('.mdi-checkbox-marked + #id_filter-all');
    cy.get('.mdi-checkbox-marked + #id_filter-1');
  });

  it('only allows deleting gyms a user has created', () => {
    cy.log('generic gym was created by admin and should not be deletable');
    cy.get('#id_menu').click();
    cy.contains($t('gymMap.deleteGym')).should('not.exist');

    cy.log('green gym was created by test user and should be deletable');
    cy.visit(`gym-map/${GREEN_GYM_NAME}`);
    waitForGymMap();
    cy.get('#id_menu').click();
    cy.contains($t('gymMap.deleteGym')).click();
    cy.contains($t('gymMap.deleteWarning', {gym: GREEN_GYM_NAME}));
    cy.contains($t('gymMap.cancel')).click();
    cy.contains($t('gymMap.deleteWarning', {gym: GREEN_GYM_NAME}))
        .should('not.exist');
  });
});

describe('The gym creation view', () => {
  beforeEach(() => {
    cy.visit('create-gym');
  });

  it('allows creating, deleting, and creating gyms again', () => {
    cy.log('create gym');
    createNewGym();

    cy.log('check that new gym can be selected in gym search');
    cy.get('.mdi-menu').click();
    cy.get('#id_find-gym').click();
    cy.contains(NEW_GYM_NAME).click();
    cy.get('.mdi-menu').click();

    cy.log('open create popover in newly created gym and submit it');
    atGymMapCoordinates(NEW_BOULDER_2_COORDINATES, ([x, y]) => {
      cy.get('#id_map-root').click(x, y);
      cy.get('#id_grade-select').click();
      cy.contains('2').click();
      cy.get('#id_color-select').click();
      cy.contains('Red').click();
      cy.contains('Save').click();
    });

    cy.log('open ascent popover and retire boulder');
    atGymMapCoordinates(NEW_BOULDER_2_COORDINATES, ([x, y]) => {
      cy.get('#id_map-root').click(x, y);
      cy.get('#id_retire-boulder').click();
    });

    cy.log('delete gym');
    cy.get('#id_menu').click();
    cy.contains($t('gymMap.deleteGym')).click();
    cy.contains($t('gymMap.deleteWarning', {gym: NEW_GYM_NAME}));
    for (const _ of waitingFor('DELETE', '/bouldern/gym/3/')) {
      cy.contains($t('gymMap.deleteGym')).click();
    }
    cy.contains($t('gymMap.gymDeleted'));
    cy.get('#id_close-notification-0').click();

    cy.log('create gym again');
    cy.visit('create-gym');
    createNewGym();
  });

  it('allows navigating to color creation view', () => {
    cy.contains('New Color').click();
    cy.get('#id_color');
  });

  it('shows errors for empty fields', () => {
    cy.get('#id_save-gym').click();
    ['gymForm.lblName', 'gymForm.lblName'].forEach((key) => {
      cy.contains($t('msgRequiredField', {field: $t(key)}));
    });
  });

  it('shows an error when grades are missing', () => {
    cy.get('#id_remove-grade-1').click();
    cy.get('#id_save-gym').click();
    cy.contains($t('msgNoGrades'));
  });

  it('allows clearing the gym map', () => {
    cy.get('#id_map').attachFile('generic_gym.png');
    cy.get('.v-file-input .mdi-close-circle').click();
  });

  it('gives a hint how to create a map', () => {
    cy.get('.v-file-input .v-messages')
        .contains($t('gymForm.createMapHint',
            {link: $t('gymForm.templateLinkText')}))
        .find('a')
        .should('have.attr', 'href')
        .and('include', 'diagrams.net');
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
    cy.get('#id_find-gym').click();
    cy.contains(GREEN_GYM_NAME).click();
    waitForGymMap();
  });

  it('allows navigating to favorite gyms', () => {
    cy.contains(GYM_NAME).click();
    waitForGymMap();
  });
});
