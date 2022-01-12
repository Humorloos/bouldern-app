import GymMapView from '../../src/views/GymMapView';

describe('The gym map view', () => {
  it('allows adding boulders', () => {
    cy.visit('login');
    cy.task('log', 'This will be output to the terminal');
    cy.window().then((win) => {
      win.$store.subscribe((mutation, state) => {
        $log[new Date().toTimeString().split(' ')[0]] = {
          mutation: mutation, state: state,
        };
      });
      // win.$store.subscribeAction((action, state) => {
      //   $log[new Date().toTimeString().split(' ')[0]] = {
      //     action: action, state: state,
      //   };
      // });
    });
    loginViaLogInLink(constants.email, constants.password);
    cy.contains(`Hello, ${constants.email}. ` +
      'You\'re at the bouldern index.');
    cy.contains('Home').click();
    cy.get('#id_gym-name').type(constants.gymName);
    cy.get('#submit_button').click();
    cy.window().its(`${GymMapView.name}.$data.loaded`).should('equal', true);
    cy.get('#map-root').click(140, 150);
    cy.contains('You clicked here');
    cy.get('#popup-closer').click();
    cy.get('#map-root').click(340, 210);
    cy.contains('Submit').click();
    cy.contains('Home').click();
    cy.task('log', $log);
  });
});
