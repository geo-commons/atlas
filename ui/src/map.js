import "tippy.js/themes/light-border.css";
import "es6-promise/auto";
import "whatwg-fetch";

import Vue from "vue";
import Vuex from "vuex";
import VueTippy, { TippyComponent } from "vue-tippy";

import { createStore } from "./store";
import { getSettingsFromPath } from "./utils/router";
import App from "./map/App";

Vue.config.productionTip = false;

Vue.use(Vuex);
Vue.use(VueTippy, {
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
Vue.component("VueTippy", TippyComponent);

// Atlas v3
document.addEventListener("DOMContentLoaded", () => {
  const el = document.querySelector("#app");
  if (!el) {
    return;
  }

  const data = JSON.parse(document.querySelector("#app-data").innerHTML);
  const settings = getSettingsFromPath(data.config);

  const layers = data.layers.map((layer) =>
    settings.visibleLayers && settings.visibleLayers.includes(layer.id)
      ? { ...layer, is_visible: true }
      : layer
  );

  const initialState = {
    isEmbed: data.is_embed,
    config: data.config,
    position: settings.position,
    layers,
    tool: "",
    selectedArea: null,
    searchQuery: "",
    alert: "",
    map: data.map,
  };

  const store = createStore(initialState);

  new Vue({
    store,
    el: "#app",
    render: (c) => c(App),
  });
});
