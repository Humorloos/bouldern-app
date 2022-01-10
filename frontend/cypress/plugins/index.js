/** @file custom handlers for cypress events */
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

/**
 * Binds handlers to events exposed by cypress
 *
 * @param on  - Is used to hook into various events Cypress emits.
 * @param config  - Is the resolved Cypress config.
 * @type {Cypress.PluginConfig}
 */
module.exports = (on, config) => {
  const options = {
    // send in the options from your webpack.config.js, so it works the same
    // as your app's code
    webpackOptions: {
      mode: 'development',
    },
    watchOptions: {},
  };
  const vueWebpackConfig = require('@vue/cli-service/webpack.config.js');
  options.webpackOptions.module = vueWebpackConfig.module;
  options.webpackOptions.plugins = vueWebpackConfig.plugins;
  options.webpackOptions.resolve = vueWebpackConfig.resolve;

  on('file:preprocessor', require('@cypress/webpack-preprocessor')(options));
  on('task', {
    log(message) {
      console.log(JSON.stringify(message, null, 2));

      return null;
    },
  });
  return config;
};
