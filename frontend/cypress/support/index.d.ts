/// <reference types="cypress" />

declare namespace Cypress {
    interface Chainable<Subject = any> {
        enterCredentialsAndLogin(): Chainable<null>;

        logInViaLogInLink(): Chainable<null>;

        verifyLogInWithInvalidUser(): Chainable<null>;
    }
}
