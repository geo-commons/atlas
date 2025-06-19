module.exports = {
  env: {
    node: true,
    es2022: true,
  },
  parser: "vue-eslint-parser",
  parserOptions: {
    parser: "@typescript-eslint/parser",
    ecmaVersion: 2020,
    sourceType: "module",
  },
  // Note: make sure prettier is the last file in the extends array,
  // as the order of the configs determine duplicate rules in different configs are handled.
  extends: [
    "eslint:recommended",
    "plugin:vue/essential",
    "plugin:vue/strongly-recommended",
    "plugin:vue/recommended",
    "plugin:@typescript-eslint/recommended",
    "prettier",
  ],
  rules: {
    // override/add rules settings here, such as:
    // 'vue/no-unused-vars': 'error'
    "vue/require-default-prop": "off",
    "vue/no-v-model-argument": "off",
    "vue/no-multiple-template-root": "off",
    "@typescript-eslint/no-unused-vars": "warn",
    "@typescript-eslint/no-explicit-any": "off",
  },
};
