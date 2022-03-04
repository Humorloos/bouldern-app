/** @file global eslint config */

module.exports = {
  env: {
    es2021: true,
    node: true,
  },
  extends: [
    'eslint:recommended',
    'google',
    'plugin:vue/vue3-recommended',
    'plugin:jsdoc/recommended',
  ],
  plugins: ['jsdoc'],
  rules: {
    'jsdoc/require-description': 2,
    'jsdoc/require-file-overview': 2,
    'jsdoc/require-jsdoc': [2, {
      require: {
        'MethodDefinition': true,
        'FunctionExpression': true,
        'ClassExpression': true,
        'ClassDeclaration': true,
      },
    }],
    'jsdoc/require-param': [2, {
      contexts: [
        // no params for store methods for now
        'FunctionDeclaration',
        'FunctionExpression' +
        ':not(CallExpression[callee.name = "createStore"] FunctionExpression)' +
        ':not(Property[key.name = "install"] FunctionExpression)',
      ],
    }],
    'jsdoc/require-param-type': 0, // for now, no types in jsdoc
    'no-unused-vars': [2, {'varsIgnorePattern': '^_$'}],
    'valid-jsdoc': 0, // eslint-jsdoc takes care of jsdoc validation
    'no-warning-comments': [2, {
      terms: ['todo'],
      location: 'anywhere',
    }],
  },
};
