/// <reference types="cypress" />

declare namespace Cypress {
    interface Chainable<> {
        enterCredentialsAndLogin(): Chainable<null>;

        logInViaLogInLink(): Chainable<null>;

        verifyLogInWithInvalidUser(): Chainable<null>;

        register(): Chainable<null>;

        registerAndLogin(): Chainable<null>;
    }
}
