/** @file custom handlers for cypress events */
/// <reference types="cypress" />
// ***********************************************************
// This example plugins/router.js can be used to load plugins
//
// You can change the location of this file or turn off loading
// the plugins file with the 'pluginsFile' configuration option.
//
// You can read more here:
// https://on.cypress.io/plugins-guide
// ***********************************************************

// This function is called when a project is opened or re-opened (e.g. due to
// the project's config changing)
const {VueLoaderPlugin} = require('vue-loader');
const fs = require('fs');

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
      module: {
        rules: [
          {
            test: /\.vue$/,
            loader: 'vue-loader',
          },
          // this will apply to both plain `.js` files
          // AND `<script>` blocks in `.vue` files
          {
            test: /\.js$/,
            loader: 'babel-loader',
          },
          // this will apply to both plain `.css` files
          // AND `<style>` blocks in `.vue` files
          {
            test: /\.css$/,
            use: [
              'vue-style-loader',
              'css-loader',
            ],
          },
        ],
      },
      plugins: [
        // make sure to include the plugin for the magic
        new VueLoaderPlugin(),
      ],
    },
    watchOptions: {},
  };

  on('file:preprocessor', require('@cypress/webpack-preprocessor')(options));
  on('task', {
    /**
     * Reads the content of the last email written by django to the
     * logs directory.
     *
     * @returns {string} the content of the last email
     */
    readLastEmail() {
      const emailPath = 'cypress/logs/email';
      const filename = fs.readdirSync(emailPath).at(-1);
      return fs.readFileSync(`${emailPath}/${filename}`, 'utf8');
    },
  });
  return config;
};
