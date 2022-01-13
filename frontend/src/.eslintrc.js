/** @file vue eslint config */

module.exports = {
  parser: 'vue-eslint-parser',
  rules: {
    'jsdoc/require-jsdoc': [2, {
      require: {
        'FunctionExpression': false,
      },
      contexts: [
        'FunctionExpression:not(' +
        'Property[key.name = /^get|set|data$/] FunctionExpression)',
      ],
    }],
  },
};
