const USERNAME = 'testUser';
const EMAIL = 'testEmail@mailprovider.com';
const PASSWORD = 'testPassword';
const COLOR_NAME = 'TestColor';
const GYM_NAME = 'testGym';
const HOST = 'http://127.0.0.1:8000';

before(() => {
    cy.exec('cd .. && python manage.py reset_db')
})

function enterCredentialsAndLogin() {
    cy.get('#id_username')
        .type(EMAIL)
        .should('have.value', EMAIL)
    cy.get('#id_password').type(PASSWORD)

    cy.get('#submit_button').contains('Log In').click()
}

function logInViaLogInLink() {
    cy.contains('You are not logged in')
    cy.contains('Log In').click()

    cy.url()
        .should('include', '/registration/login')

    enterCredentialsAndLogin();
}

describe('The register app', () => {
    it('notifys correctly if user does not exist', () => {
        // try log in with non-existent user
        cy.visit(`${HOST}/bouldern`)

        logInViaLogInLink();

        cy.contains('Please enter a correct email and password.')
    })

    it('lets users log in once they have signed up', () => {
        // Sign up
        cy.visit(`${HOST}/registration/signup`)

        cy.get('#id_username')
            .type(USERNAME)
            .should('have.value', USERNAME)
        cy.get('#id_email')
            .type(EMAIL)
            .should('have.value', EMAIL)
        cy.get('#id_password1').type(PASSWORD)
        cy.get('#id_password2').type(PASSWORD)
        cy.get('#submit_button').contains('Sign Up').click()
        // cy.pause()

        // Log in after signing up
        enterCredentialsAndLogin()
    })
    it('lets users log out and log in again', () => {
        // Sign out
        cy.contains('Log Out').click()

        logInViaLogInLink()
    })
    it('lets users add new colors', () => {
        // add gym
        cy.visit(`${HOST}/bouldern/add-gym`)
        cy.contains('New Color').click()
        cy.get('div.jquery-modal #id_name').type(COLOR_NAME);
        cy.get('#id_color').click()
        cy.get('div[style="background: rgba(255, 0, 0, 0.2); opacity: 0; position: absolute; left: 0px; top: 0px; width: 245px; height: 176px; cursor: crosshair;"]')
            .click(150, 50)
        cy.get('div.jquery-modal #submit_button').click()

        cy.get('#difficulty-level').click()
        cy.contains(COLOR_NAME).click()
        cy.pause()

        cy.get('#delete_account').click()

    })
})
