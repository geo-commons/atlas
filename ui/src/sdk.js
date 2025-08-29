import "vite/modulepreload-polyfill";
import "tippy.js/dist/tippy.css";
import "es6-promise/auto";
import "whatwg-fetch";
import { createApp } from "vue";
import VueTippy from "vue-tippy";

import App from "./sdk/pages/App.vue";

const Map = class {
  constructor(target, props) {
    this.renderMap(target, props);
  }

  renderMap(target, props) {
    const app = createApp(App, props);
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
    this.vm = app.mount(target);
  }

  addInteraction(name, options) {
    return this.vm.addInteraction(name, options);
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
