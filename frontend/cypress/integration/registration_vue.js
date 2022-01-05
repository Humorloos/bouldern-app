// todo: check if I can import this in index support too
import {constants} from '../support/constants';
describe('The register vue app', () => {
  it('notifys correctly if user does not exist', function() {
    cy.visit(`${constants.hostVue}/`);
    cy.contains('Log In').click();
    // try log in with non-existent user
    cy.logInViaLogInLinkNew();
    cy.contains(cy.t('wrongCredentialsMsg'));
    cy.contains('Home').click();
  });

  it('allows logging in after registering', () => {
    cy.registerAndLoginVue();
  });
  it('allows logging out', () => {
    cy.contains('Log Out').click();
    cy.contains('Log In').click();
    cy.contains(messages.notLoggedInMsg);
  });
});
