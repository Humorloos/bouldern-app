/// <reference types="cypress" />

declare namespace Cypress {
    interface Chainable<> {
        logInViaLogInLinkNew(): Chainable<null>;

        logInViaLogInLink(): Chainable<null>;
    }
}
