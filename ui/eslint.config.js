const js = require("@eslint/js");
const vue = require("eslint-plugin-vue");
const vueParser = require("vue-eslint-parser");
const globals = require("globals");
const tseslint = require("typescript-eslint");
const prettier = require("eslint-plugin-prettier/recommended");

module.exports = [
  {
    ignores: ["node_modules/**", "dist/**", "*.config.*"],
  },
  js.configs.recommended,
  ...vue.configs["flat/recommended"],
  ...tseslint.configs.recommended,
  {
    files: ["**/*.{js,ts,vue}"],
    languageOptions: {
      ecmaVersion: 2022,
      sourceType: "module",
      globals: {
        ...globals.browser,
      },
      parser: vueParser,
      parserOptions: {
        parser: tseslint.parser,
      },
    },
    rules: {
      "vue/require-default-prop": "off",
      "vue/no-v-model-argument": "off",
      "vue/no-multiple-template-root": "off",
      "@typescript-eslint/no-unused-vars": "warn",
      "@typescript-eslint/no-explicit-any": "off",
    },
  },
  prettier,
];
