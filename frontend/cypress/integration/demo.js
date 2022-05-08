/** @file cypress test for taking google play screenshots */

import {
  GYM_NAME,
  NEW_BOULDER_2_COORDINATES,
  NEW_GYM_NAME,
} from '../support/constants.js';
import {
  atGymMapCoordinates,
  login,
  panMap,
  waitForGymMap,
  waitingFor,
} from '../support/functions.js';


describe('The boulder holder', () => {
  it('allows taking screenshot for the app listings', () => {
    cy.log('log in');
    login();

    cy.log('open gym map');
    cy.visit(`gym-map/${GYM_NAME}`);
    waitForGymMap();

    cy.log('take screenshot of gym map');
    panMap(70, 0);
    cy.screenshot('1-gym-map', {
      capture: 'viewport',
      overwrite: true,
    });

    cy.log('take screenshot of create popover');
    atGymMapCoordinates(NEW_BOULDER_2_COORDINATES, ([x, y]) => {
      cy.get('#id_map-root').click(x, y);
      cy.get('#id_grade-select').click();
      cy.contains('5').click();
      cy.get('#id_color-select').click();
      cy.contains('Yellow').click();
      cy.screenshot('2-create-boulder', {
        capture: 'viewport',
        overwrite: true,
      });
      cy.contains('Save').click();
    });

    cy.log('take screenshot of edit popover');
    atGymMapCoordinates(NEW_BOULDER_2_COORDINATES, ([x, y]) => {
      cy.get('#id_map-root').click(x, y);
      cy.contains($t('gymMap.ascentResults[0]')).click();
      cy.screenshot('3-report-ascent', {
        capture: 'viewport',
        overwrite: true,
      });
      cy.get('#save-boulder').click();
    });

    cy.log('take screenshot of creating gyms');
    cy.visit('create-gym');
    cy.get('#id_name').type(NEW_GYM_NAME);
    cy.get('#id_map').attachFile('generic_gym.png');
    cy.get('img').should('be.visible');
    cy.screenshot('4-create-gym', {
      capture: 'viewport',
      overwrite: true,
    });

    cy.log('take another screenshot of creating gyms');
    cy.get('#id_color-grade-1').click();
    cy.contains('Yellow').click();
    cy.contains('Add Grade').click();
    cy.get('#id_color-grade-2').click();
    cy.contains('Red').click();
    cy.contains('Add Grade').click();
    cy.scrollTo('bottom');
    cy.screenshot('5-create-gym-2', {
      capture: 'viewport',
      overwrite: true,
    });
    cy.get('#id_remove-grade-3').click();
    for (const _ of waitingFor('/bouldern/gym')) {
      for (const _ of waitingFor('/bouldern/gym/3')) {
        cy.get('#id_save-gym').click();
      }
    }
    waitForGymMap();

    cy.log('take screenshot of the gym search');
    cy.get('.mdi-menu').click();
    cy.get('#id_find-gym').click().type(NEW_GYM_NAME.charAt(0));
    cy.screenshot('6-find-gym', {
      capture: 'viewport',
      overwrite: true,
    });
  });
});
