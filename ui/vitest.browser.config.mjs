import { defineProject, mergeConfig } from "vitest/config";
import viteConfig from "./vite.config.mjs";
import { playwright } from "@vitest/browser-playwright";

export default mergeConfig(
  viteConfig,
  defineProject({
    test: {
      name: "browser",
      include: ["tests/browser/**/*.{test,spec}.ts"],
      browser: {
        enabled: true,
        provider: playwright(),
        instances: [{ browser: "chromium", headless: true }],
      },
    },
  }),
);
