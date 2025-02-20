import "vite/modulepreload-polyfill";
import "tippy.js/dist/tippy.css";
import "es6-promise/auto";
import "whatwg-fetch";

import { createApp } from "vue";
import VueTippy from "vue-tippy";

import { getSettingsFromPath } from "./utils/router";
import App from "./map/App";
import { useGlobalStore } from "@/stores";
import { createPinia } from "pinia";
import PrimeVue from "primevue/config";
import { AtlasPresetApp } from "@/utils/theme-preset";

// Atlas v3
document.addEventListener("DOMContentLoaded", () => {
  const el = document.querySelector("#app");
  if (!el) {
    return;
  }

  const data = JSON.parse(document.querySelector("#app-data").innerHTML);
  const settings = getSettingsFromPath(data.config);

  const allAvailableLayers = data.layers;
  const configuredLayers = data.map.layers;
  // First set custom settings as configured by user.
  let layers = configuredLayers.map((configuredLayer) => {
    const defaultLayer = allAvailableLayers.find((layer) => layer.internal_id === configuredLayer.layer);

    if (configuredLayer.settings.customSettings) {
      return {
        ...defaultLayer,
        is_visible: configuredLayer.settings.is_visible,
        is_base: configuredLayer.settings.is_base,
        opacity: configuredLayer.settings.opacity,
        zoom_min: configuredLayer.settings.zoom_min,
        zoom_max: configuredLayer.settings.zoom_max,
        display_properties: configuredLayer.settings.display_properties,
        search_fields: configuredLayer.settings.search_fields,
        server_style: configuredLayer.settings.server_style,
        client_style: configuredLayer.settings.client_style,
        friendly_fields: configuredLayer.settings.friendly_fields,
        templated_properties: configuredLayer.settings.templated_properties,
        linked_data: configuredLayer.settings.linked_data,
        templates: configuredLayer.settings.templates,
      };
    } else {
      return defaultLayer;
    }
  });

  // Check if there is at least 1 base layer configured.
  const hasBaseLayer = layers.some((layer) => layer.is_base);

  if (!hasBaseLayer) {
    // If there is no base layer configured get the first available and add is to layers.
    const baseLayer = allAvailableLayers.find((layer) => layer.is_base);
    layers.push(baseLayer);
  }

  // Then check if any specific settings are set by the URL settings.
  layers = layers.map((layer) => {
    if (!layer) {
      return {};
    }

    if (layer.is_base) {
      return {
        ...layer,
        is_visible: settings.visibleBase ? settings.visibleBase === layer.id : layer.is_visible,
      };
    }

    if (!layer.is_base) {
      return {
        ...layer,
        is_visible: settings.visibleLayers.length ? settings.visibleLayers.includes(layer.id) : layer.is_visible,
      };
    }
  });

  const initialState = {
    isEmbed: data.is_embed,
    config: data.config,
    user: data.user,
    position: settings.position,
    layers,
    tool: "",
    selectedArea: null,
    searchQuery: "",
    alert: "",
    map: data.map,
  };

  const pinia = createPinia();

  // Note: darkModeSelector is set to "light" until we implement dark mode.
  const app = createApp(App)
    .use(PrimeVue, {
      theme: {
        preset: AtlasPresetApp,
        options: {
          prefix: "prime",
          darkModeSelector: "light",
          cssLayer: false,
        },
      },
    })
    .use(pinia)
    .use(VueTippy, {
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

  const piniaStore = useGlobalStore();
  piniaStore.setInitialState(initialState);

  app.mount("#app");
});
