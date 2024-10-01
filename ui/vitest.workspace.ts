// vitest.workspace.ts
import { defineWorkspace } from "vitest/config";

export default defineWorkspace([
  {
    extends: "./vite.config.mjs",
    test: {
      include: ["tests/unit/**/*.{test,spec}.ts", "tests/**/*.unit.{test,spec}.ts"],
      name: "unit",
      environment: "node",
    },
  },
  {
    extends: "./vite.config.mjs",
    test: {
      include: ["tests/browser/**/*.{test,spec}.ts", "tests/**/*.browser.{test,spec}.ts"],
      name: "browser",
      browser: {
        enabled: true,
        name: "chromium",
        headless: true,
        provider: "playwright",
      },
    },
  },
]);
