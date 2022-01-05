/// <reference types="cypress" />

declare namespace Cypress {
    interface Chainable<> {
        enterNewCredentialsAndLogin(): Chainable<null>;

        enterCredentialsAndLogin(): Chainable<null>;

        logInViaLogInLinkNew(): Chainable<null>;

        logInViaLogInLink(): Chainable<null>;

        register(): Chainable<null>;

        registerAndLogin(): Chainable<null>;

        openNewGymMap(): Chainable<null>;

        openGymMap(): Chainable<null>;
    }
}
