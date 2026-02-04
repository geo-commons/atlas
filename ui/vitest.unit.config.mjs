import { defineProject, mergeConfig } from "vitest/config";
import viteConfig from "./vite.config.mjs";

export default mergeConfig(
  viteConfig,
  defineProject({
    test: {
      name: "unit",
      include: ["tests/unit/**/*.{test,spec}.ts"],
      environment: "node",
    },
  }),
);
