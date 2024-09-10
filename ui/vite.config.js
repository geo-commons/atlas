import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
const path = require("path");

export default defineConfig({
  plugins: [vue()],
  base: "/atlas/static/",
  build: {
    outDir: path.resolve(__dirname, "../static/atlas"),
    manifest: true,
    rollupOptions: {
      input: {
        app: path.resolve(__dirname, "src/app.js"),
        admin: path.resolve(__dirname, "src/admin.js"),
        map: path.resolve(__dirname, "src/map.js"),
        tables: path.resolve(__dirname, "src/tables.js"),
        portal: path.resolve(__dirname, "src/portal.js"),
        css: path.resolve(__dirname, "src/assets/styles/main.css.js"),
      },
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
    extensions: [".mjs", ".js", ".ts", ".jsx", ".tsx", ".json", ".vue"],
  },
});
