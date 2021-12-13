before(() => {
    cy.exec('cd .. && python manage.py reset_db')
})
beforeEach(() => {
    // before each test, we can automatically preserve the
    // 'session_id' and 'remember_token' cookies. this means they
    // will not be cleared before the NEXT test starts.
    //
    // the name of your cookies will likely be different
    // this is an example
    Cypress.Cookies.preserveOnce('sessionid', 'csrftoken')
})

describe('The register app', () => {
    it('notifys correctly if user does not exist', () => {
        // try log in with non-existent user
        cy.visit(`${Cypress.env('host')}/bouldern`)

        cy.logInViaLogInLink();

        cy.contains('Please enter a correct email and password.')
    })

    it('lets users log in once they have signed up', () => {
        // Sign up
        cy.visit(`${Cypress.env('host')}/registration/signup`)

        cy.get('#id_username')
            .type(Cypress.env('username'))
            .should('have.value', Cypress.env('username'))
        cy.get('#id_email')
            .type(Cypress.env('email'))
            .should('have.value', Cypress.env('email'))
        cy.get('#id_password1').type(Cypress.env('password'))
        cy.get('#id_password2').type(Cypress.env('password'))
        cy.get('#submit_button').contains('Sign Up').click()
        // cy.pause()

        // Log in after signing up
        cy.enterCredentialsAndLogin()
    })
    it('lets users log out and log in again', () => {
        // Sign out
        cy.contains('Log Out').click()

        cy.logInViaLogInLink()
    })
})
