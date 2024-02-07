import "tippy.js/dist/tippy.css";
import "es6-promise/auto";
import "whatwg-fetch";

import Vue from "vue";
import Vuex from "vuex";
import VueTippy from "vue-tippy";

import App from "./pages/App";
import LegacyEmbedModal from "./pages/LegacyEmbedModal";
import { createStore } from "./store";
import { getSettingsFromPath } from "./utils/router";
import { isMobile } from "./utils/helpers";
import detectKeyboard from "./utils/detect-keyboard";

Vue.use(Vuex);
Vue.config.productionTip = false;

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

// Atlas v3
document.addEventListener("DOMContentLoaded", () => {
  const el = document.querySelector("#app");
  if (!el) {
    return;
  }

  const data = JSON.parse(document.querySelector("#app-data").innerHTML);
  const settings = getSettingsFromPath(data.config);

  const layers = data.layers.map((layer) => {
    if (layer.is_base) {
      return {
        ...layer,
        is_visible: settings.visibleBase ? settings.visibleBase == layer.id : layer.is_visible,
      };
    }

    if (!layer.is_base) {
      return {
        ...layer,
        is_visible: settings.visibleLayers ? settings.visibleLayers.includes(layer.id) : layer.is_visible,
      };
    }
  });

  const initialState = {
    isEmbed: data.is_embed,
    config: data.config,
    position: settings.position,
    drawing: settings.drawing,
    layers,
    tool: "",
    user: data.user,
    selectedArea: null,
    initiallyShowLayerList: settings.visibleLayers.length === 0 && !isMobile() && !data.is_embed,
    searchQuery: "",
    alert: "",
  };

  const store = createStore(initialState);

  new detectKeyboard();

  // todo: change to #424bff once color is changed in main application
  Vue.prototype.$primaryColor = "#0066FF";

  new Vue({
    el: "#app",
    store,
    render: (c) => c(App),
  });
});

// Embed map in jQuery frontend
document.addEventListener("DOMContentLoaded", () => {
  const el = document.querySelector("#embedCode");
  if (!el) {
    return;
  }

  const data = JSON.parse(document.querySelector("#app-data").innerHTML);
  const settings = getSettingsFromPath(data.config);

  const initialState = {
    isEmbed: data.is_embed,
    config: data.config,
    position: settings.position,
    drawing: settings.drawing,
    layers: [],
    tool: "",
    selectedArea: null,
    searchQuery: "",
    alert: "",
  };

  const store = createStore(initialState);
  window.vueStore = store; // assign store to window for interoperability with old jQuery frontend

  // todo: change to #424bff once color is changed in main application
  Vue.prototype.$primaryColor = "#0066FF";

  new Vue({
    el: "#embedCode",
    store,
    render: (c) => c(LegacyEmbedModal),
  });
});
