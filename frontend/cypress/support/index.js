/**
 *  @file this file is called before executing each e2e test and executes code
 *  required in multiple e2e tests
 */

// ***********************************************************
// This example support/index.js is processed and
// loaded automatically before your test files.
//
// This is a great place to put global configuration and
// behavior that modifies Cypress.
//
// You can change the location of this file or turn off
// automatically serving support files with the
// 'supportFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/configuration
// ***********************************************************

import './functions';
import './constants';
import 'cypress-file-upload';

cy.$log = {};

before(() => {
  cy.exec('cd .. && python manage.py reset_db');
});
