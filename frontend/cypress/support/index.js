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
import 'cypress-wait-until';
import {EMAIL, PASSWORD} from './constants.js';
import {slugify} from './functions.js';

require('cypress-terminal-report/src/installLogsCollector')();

before(() => {
  // reset DB
  cy.exec('cd .. && python manage.py reset_db');
  // get login data
  cy.request('POST', 'https://localhost:8000/registration/login/', {
    email: EMAIL,
    password: PASSWORD,
  }).its('body')
      .then((res) => {
        cy.loginData = res;
      });
});

beforeEach(() => {
  cy.$log = {};
});

afterEach(() => {
  cy.writeFile(`cypress/logs/vuex/${Cypress.currentTest.titlePath.map(slugify).
      join('/')}.json`, cy.$log);
});
