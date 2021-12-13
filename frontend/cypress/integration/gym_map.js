before(() => {
    cy.exec('cd .. && python manage.py reset_db')
})

describe('The register app', () => {
    it('lets users add new colors', () => {
        // add gym
        cy.visit(`${Cypress.env('HOST')}/bouldern/add-gym`)
        cy.contains('New Color').click()
        cy.get('div.jquery-modal #id_name').type(Cypress.env('colorName'));
        cy.get('#id_color').click()
        cy.get('div[style="background: rgba(255, 0, 0, 0.2); opacity: 0; position: absolute; left: 0px; top: 0px; width: 245px; height: 176px; cursor: crosshair;"]')
            .click(150, 50)
        cy.get('div.jquery-modal #submit_button').click()

        cy.get('#difficulty-level').click()
        cy.contains(Cypress.env('colorName')).click()
    })
    it('lets users create new gyms', () => {
        cy.get('#id_name').type(Cypress.env('gymName'))
        cy.get('#id_map').attachFile('generic_gym.png')
        cy.contains('Add Level').click()
        cy.get('#difficulty-level:nth-of-type(2)').click()
        cy.contains('Yellow').click()
        cy.contains('Submit').click()
        cy.contains("You're at the bouldern index")
    })
    it('can add boulders to gyms', () => {
        cy.visit(`${Cypress.env('host')}/bouldern/${Cypress.env('gymName')}/map`)
        cy.get('#testGym_div_map').click(350, 150)
        cy.pause()

        cy.get('#delete_account').click()

    })
})
