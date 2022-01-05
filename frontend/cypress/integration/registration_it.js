describe('The register vue app', () => {
  it('notifys correctly if user does not exist', function() {
    cy.visit(`${constants.hostVue}/`);
    cy.contains('Log In').click();
    // try log in with non-existent user
    cy.logInViaLogInLinkNew();
    cy.contains($t('wrongCredentialsMsg'));
    cy.contains('Home').click();
  });

  it('allows logging in after registering', () => {
    cy.registerAndLogin();
  });
  it('allows logging out', () => {
    cy.contains('Log Out').click();
    cy.contains('Log In').click();
    cy.contains($t('notLoggedInMsg'));
  });
  it('allows deleting your account', () => {
    // try log in with non-existent user
    cy.logInViaLogInLinkNew();
    cy.contains('Home').click();
    cy.contains('Delete Account').click();
    cy.contains('Log In').click();
    cy.logInViaLogInLinkNew();
    cy.contains($t('wrongCredentialsMsg'));
  });
});
