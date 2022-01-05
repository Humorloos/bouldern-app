/// <reference types="cypress" />

declare namespace Cypress {
    interface Chainable<> {
        enterNewCredentialsAndLogin(): Chainable<null>;

        enterCredentialsAndLogin(): Chainable<null>;

        logInViaLogInLink(): Chainable<null>;

        logInViaLogInLinkNew(): Chainable<null>;

        logInViaLogInLinkVue(): Chainable<null>;

        verifyLogInWithInvalidUser(): Chainable<null>;

        register(): Chainable<null>;

        registerAndLogin(): Chainable<null>;

        registerAndLoginVue(): Chainable<null>;

        openNewGymMap(): Chainable<null>;

        openGymMap(): Chainable<null>;
    }
}
