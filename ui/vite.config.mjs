import { defineConfig } from "vite";
import vue from "@vitejs/plugin-vue";
import svgLoader from "vite-svg-loader";
import path from "path";

export default defineConfig({
  plugins: [
    vue({
      template: {
        compilerOptions: {
          compatConfig: {
            MODE: 2
          }
        }
      }
    }),
    svgLoader({ defaultImport: "component" })
  ],
  base: "/atlas/static/",
  build: {
    outDir: path.resolve(__dirname, "../static/atlas"),
    manifest: true,
    assetsInlineLimit: 0,
    rollupOptions: {
      input: {
        app: path.resolve(__dirname, "src/app.js"),
        admin: path.resolve(__dirname, "src/admin.js"),
        map: path.resolve(__dirname, "src/map.js"),
        tables: path.resolve(__dirname, "src/tables.js"),
        portal: path.resolve(__dirname, "src/portal.js"),
      },
    },
  },
  resolve: {
    alias: {
      "vue": "@vue/compat",
      "@": path.resolve(__dirname, "./src"),
    },
    extensions: [".mjs", ".js", ".ts", ".jsx", ".tsx", ".json", ".vue"],
  },
  server: {
    origin: 'http://localhost:5173',
    port: 5173,
    strictPort: true,
    hmr: {
      protocol: 'ws',
      host: 'localhost',
    },
  },
});