/** @file vue eslint config */

module.exports = {
  parser: 'vue-eslint-parser',
  rules: {
    'vue/multi-word-component-names': 0,
    'jsdoc/require-jsdoc': [2, {
      require: {
        'FunctionExpression': false,
      },
      contexts: [
        'FunctionExpression:not(' +
        'Property[key.name = /^get$|^set.*$|^data$|^setup$/]' +
        ' FunctionExpression)',
      ],
    }],
    'jsdoc/require-param': [0, {
      checkDestructured: false,
    }],
  },
};
