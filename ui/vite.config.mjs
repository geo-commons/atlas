import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import svgLoader from "vite-svg-loader";
import Components from "unplugin-vue-components/vite";
import { PrimeVueResolver } from "@primevue/auto-import-resolver";
import path from "path";

export default defineConfig({
  plugins: [
    vue(),
    Components({
      resolvers: [PrimeVueResolver()],
    }),
    svgLoader({ defaultImport: "component" }),
  ],
  base: "/atlas/static/",
  build: {
    outDir: path.resolve(__dirname, "../homepage/static/dist"),
    manifest: "manifest.json",
    assetsInlineLimit: 0,
    rollupOptions: {
      input: {
        app: path.resolve(__dirname, "src/app.js"),
        admin: path.resolve(__dirname, "src/admin.js"),
        map: path.resolve(__dirname, "src/map.js"),
        tables: path.resolve(__dirname, "src/tables.js"),
        portal: path.resolve(__dirname, "src/portal.js"),
        notFound: path.resolve(__dirname, "src/not_found.js"),
      },
    },
  },
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
    extensions: [".mjs", ".js", ".ts", ".jsx", ".tsx", ".json", ".vue"],
  },
  server: {
    origin: "http://localhost:5173",
    port: 5173,
    strictPort: true,
    hmr: {
      protocol: "ws",
      host: "localhost",
    },
  },
  test: {
    projects: ["./vitest.unit.config.mjs", "./vitest.browser.config.mjs"],
  },
});
