/** @file global eslint config */

module.exports = {
  'env': {
    'node': true,
  },
  'parser': '@babel/eslint-parser',
  'extends': [
    'eslint:recommended',
    'google',
    'plugin:vue/vue3-recommended',
    'plugin:jsdoc/recommended',
  ],
  'plugins': ['jsdoc'],
  'rules': {
    'jsdoc/require-file-overview': 2,
    'valid-jsdoc': 0, // eslint-jsdoc takes care of jsdoc validation
    'jsdoc/require-jsdoc': [2, {
      require: {
        'MethodDefinition': true,
        'FunctionExpression': true,
        'ClassExpression': true,
        'ClassDeclaration': true,
        'ArrowFunctionExpression': true,
      },
    }],
    'jsdoc/require-description': 2,
    'jsdoc/require-param': [2, {
      contexts: [
        // no params for store methods for now
        'ArrowFunctionExpression:not(' +
        'CallExpression[callee.name ="createStore"] ArrowFunctionExpression)',
        'FunctionDeclaration',
        'FunctionExpression:not(' +
        'CallExpression[callee.name ="createStore"] FunctionExpression)',
      ],
    }],
    'jsdoc/require-param-type': 0, // for now, no types in jsdoc
  },
};
