'use strict';

const pages = {
  'index': {
    // entry for the page
    entry: 'src/main.js',
    // the source template
    template: 'public/index.html',
    // output as dist/index.html
    filename: 'index.html',
    // when using title option, template title tag needs to be
    // <title><%= htmlWebpackPlugin.options.title %></title>
    title: 'Index Page',
    // chunks to include on this page, by default includes
    // extracted common chunks and vendor chunks.
    chunks: ['chunk-vendors', 'chunk-common', 'index'],
  },
};

const path = require('path');

module.exports = {
  pages: pages,
  filenameHashing: false, // Django will hash file names, not webpack
  // Setting this to false can speed up production builds if you don't need
  // source maps for production.
  productionSourceMap: false,
  publicPath: process.env.NODE_ENV === 'production' ?
    // signals to django-webpack-loader to fall back to Django's standard
    // static finder behavior
    '' :
    'https://localhost:8080/', // in development, use own webpack development server
  // outputDir must be added to Django's TEMPLATE_DIRS
  outputDir: path.resolve(__dirname, 'dist/'),
  // assetsDir must match Django's STATIC_URL
  assetsDir: 'static',
  configureWebpack: {
    // This setting is for loading i18n yaml files
    module: {
      rules: [
        {
          test: /\.ya?ml$/,
          type: 'json', // Required by Webpack v4
          use: 'yaml-loader',
        },
      ],
    },
  },
  chainWebpack: (config) => {
    // extract vendor javascripts into single shared bundle to allow browsers to
    // cache common javascript
    config.optimization
        .splitChunks({
          cacheGroups: {
            vendor: {
              test: /[\\/]node_modules[\\/]/,
              name: 'chunk-vendors',
              chunks: 'all',
              priority: 1,
            },
          },
        });

    config.devServer
        .public('https://localhost:8080')
        .host('localhost')
        .port(8080)
        .hotOnly(true)
        .watchOptions({poll: 1000})
        .https(true) // https is needed for dj-rest-auth
        .historyApiFallback(true); // needed for vue router history
  },
};
