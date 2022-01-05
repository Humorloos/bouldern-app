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
      module: {
        rules: [
          {
            test: /\.jsx?$/,
            exclude: [/node_modules/],
            use: [{
              loader: 'babel-loader',
              options: {
                presets: ['@babel/preset-env'],
              },
            }],
          },
          {
            test: /\.ya?ml$/,
            type: 'json', // Required by Webpack v4
            use: 'yaml-loader',
          },
        ],
      },
    },
    watchOptions: {},
  };

  // eslint-disable-next-line @typescript-eslint/no-var-requires
  on('file:preprocessor', require('@cypress/webpack-preprocessor')(options));
  return config;
};
