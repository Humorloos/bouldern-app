'use strict';
const BundleTracker = require('webpack-bundle-tracker');

const pages = {
  'gym_form': {
    entry: './src/gym_form.js',
    chunks: ['chunk-vendors'],
  },
  'gym_map': {
    entry: './src/gym_map.js',
    chunks: ['chunk-vendors'],
  },
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
    // delete plugins that create html files for bundles since we serve them
    // from django templates
    ['gym_form', 'gym_map'].forEach((page) => {
      config.plugins.delete(`html-${page}`);
      config.plugins.delete(`preload-${page}`);
      config.plugins.delete(`prefetch-${page}`);
    });

    // webpack-stats.json is created by BundleTracker and describes bundles
    // produced by build process
    config
        .plugin('BundleTracker')
        .use(BundleTracker, [{filename: '../frontend/webpack-stats.json'}]);

    // __STATIC__ alias allows referencing paths to static files within Vue
    // components as "~__STATIC__/logo.png"
    config.resolve.alias
        .set('__STATIC__', 'static');

    config.devServer
        .public('https://localhost:8080')
        .host('localhost')
        .port(8080)
        .hotOnly(true)
        .watchOptions({poll: 1000})
        .https(true) // https is needed for dj-rest-auth
        .headers({'Access-Control-Allow-Origin': ['*']})
        .historyApiFallback(true);
  },
};
