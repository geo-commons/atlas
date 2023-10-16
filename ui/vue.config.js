const BundleTracker = require("webpack-bundle-tracker");
const path = require("path");
const DEPLOYMENT_PATH = "/atlas/static/dist/";

module.exports = {
  publicPath: process.env.NODE_ENV === "production" ? DEPLOYMENT_PATH : "http://localhost:8081/",
  outputDir: "../homepage/static/dist",

  devServer: {
    port: 8081,
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
  },

  chainWebpack: (config) => {
    config.module.rules.delete("svg");
  },
  configureWebpack: {
    plugins: [new BundleTracker({ path: __dirname, filename: "webpack-stats.json" })],
    module: {
      rules: [
        {
          test: /\.svg$/,
          include: [path.resolve(__dirname, "src/assets/icons")],
          loader: "vue-svg-loader",
        },
      ],
    },
  },

  css: {
    sourceMap: true,
  },

  pages: {
    app: { entry: "src/app.js" },
    map: { entry: "src/map.js" },
    admin: { entry: "src/admin.js" },
    tables: { entry: "src/tables.js" },
    portal: { entry: "src/portal.js" },
  },
};
