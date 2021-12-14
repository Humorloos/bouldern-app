'use strict';
const BundleTracker = require('webpack-bundle-tracker');

const pages = {
  'gym_form': {
    entry: './src/gym_form.js',
    chunks: ['chunk-vendors'],
  },
};

const path = require('path');

module.exports = {
  pages: pages,
  filenameHashing: false, // Django will hash file names, not webpack
  productionSourceMap: false,
  publicPath: process.env.NODE_ENV === 'production' ?
      // signals to django-webpack-loader to fall back to Django's standard
      // static finder behavior
      '' :
      'http://localhost:8080/', // in development, use own webpack development server
  outputDir: path.resolve(__dirname, '../python_anywhere/static/vue/'),
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
    Object.keys(pages).forEach((page) => {
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
        .public('http://localhost:8080')
        .host('localhost')
        .port(8080)
        .hotOnly(true)
        .watchOptions({poll: 1000})
        .https(false)
        .headers({'Access-Control-Allow-Origin': ['*']});
  },
};
