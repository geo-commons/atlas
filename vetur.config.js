// vetur.config.js
/** @type {import('vls').VeturConfig} */
module.exports = {
  settings: {
    "vetur.useWorkspaceDependencies": true,
    "vetur.experimental.templateInterpolationService": true,
  },
  // support monorepos
  projects: [
    "./ui", // Shorthand for specifying only the project root location
    {
      root: "./ui",
      package: "./package.json",
      snippetFolder: "./.vscode/vetur/snippets",
      globalComponents: ["./src/components/**/*.vue"],
    },
  ],
};
