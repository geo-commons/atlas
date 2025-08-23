import "vite/modulepreload-polyfill";
import "tippy.js/dist/tippy.css";
import "es6-promise/auto";
import "whatwg-fetch";
import { createApp } from "vue";
import VueTippy from "vue-tippy";

import App from "./sdk/pages/App.vue";

const Map = class {
  constructor(target, settings) {
    this.renderMap(target, settings);
  }

  async renderMap(target, settings) {
    const app = createApp(App, settings);
    app.use(VueTippy, {
      directive: "tippy",
      distance: 5,
      placement: "top",
      duration: [200, 175],
      hideOnClick: true,
      interactive: true,
      ignoreAttributes: true,
      allowHTML: false,
      boundary: "viewport",
      delay: [1000, 0],
    });
    app.mount(target);
  }
};

window.atlas = {
  Map,
};

window.addEventListener("DOMContentLoaded", () => {
  if (window.initAtlas) {
    window.initAtlas();
  }
});
