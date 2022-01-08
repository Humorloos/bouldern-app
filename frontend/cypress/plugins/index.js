/* eslint-disable @typescript-eslint/no-var-requires */
/// <reference types="cypress" />
// ***********************************************************
// This example plugins/index.js can be used to load plugins
//
// You can change the location of this file or turn off loading
// the plugins file with the 'pluginsFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/plugins-guide
// ***********************************************************

// This function is called when a project is opened or re-opened (e.g. due to
// the project's config changing)
module.exports = (on, config) => {
  /**
   * @param on is used to hook into various events Cypress emits
   * @param config is the resolved Cypress config
   * @type {Cypress.PluginConfig}
   */
  const options = {
    // send in the options from your webpack.config.js, so it works the same
    // as your app's code
    webpackOptions: {
      mode: 'development',
    },
    watchOptions: {},
  };
  options.webpackOptions.module =
    require('@vue/cli-service/webpack.config.js').module;

  on('file:preprocessor', require('@cypress/webpack-preprocessor')(options));
  return config;
};
