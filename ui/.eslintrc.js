module.exports = {
  env: {
    node: true,
  },
  // Note: make sure prettier is the last file in the extends array,
  // as the order of the configs determine duplicate rules in different configs are handled.
  extends: [
    "eslint:recommended",
    "plugin:vue/essential",
    "plugin:vue/strongly-recommended",
    "plugin:vue/recommended",
    "prettier",
  ],
  rules: {
    // override/add rules settings here, such as:
    // 'vue/no-unused-vars': 'error'
    "vue/require-default-prop": "off",
  },
};
