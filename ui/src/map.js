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
import { ConfirmationService, ToastService } from "primevue";
import { AtlasPreset } from "@/utils/theme-preset";
import { buildCategoryTree, flattenCategoryTreeLayers } from "@/utils/map-layer-tree";

const getCategoriesFromLayers = (layers) => {
  const categoriesById = new Map();

  layers.forEach((layer) => {
    if (!layer?.category) {
      return;
    }

    categoriesById.set(layer.category.id, layer.category);

    if (layer.category.parent) {
      categoriesById.set(layer.category.parent.id, layer.category.parent);
    }
  });

  return [...categoriesById.values()];
};

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
    const configuredSettings = configuredLayer.settings ?? {};
    const mapLayerSettings = {
      is_base: Boolean(configuredSettings.is_base),
    };

    if (configuredSettings.customSettings) {
      // Override with custom settings, as far as they are present
      const overrideKeys = [
        "is_visible",
        "is_filterable_in_legend",
        "opacity",
        "zoom_min",
        "zoom_max",
        "display_properties",
        "search_fields",
        "server_style",
        "client_style",
        "friendly_fields",
        "templated_properties",
        "linked_data",
        "templates",
      ];

      return {
        ...defaultLayer,
        ...mapLayerSettings,
        ...Object.fromEntries(
          overrideKeys
            .filter((key) => Object.hasOwn(configuredSettings, key))
            .map((key) => [key, configuredSettings[key]]),
        ),
      };
    } else {
      return {
        ...defaultLayer,
        ...mapLayerSettings,
      };
    }
  });

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
        is_visible: settings.visibleLayers?.length > 0 ? settings.visibleLayers.includes(layer.id) : layer.is_visible,
      };
    }
  });

  const layerOrdering = new Map(configuredLayers.map((layer) => [layer.layer, layer.ordering]));
  const layerTree = buildCategoryTree(
    layers.filter((layer) => layer && !layer.is_base),
    getCategoriesFromLayers(allAvailableLayers),
    data.map.categories || [],
    layerOrdering,
  );
  layers = [...layers.filter((layer) => layer?.is_base), ...flattenCategoryTreeLayers(layerTree)];

  const initialState = {
    isEmbed: settings.is_embed,
    config: data.config,
    user: data.user,
    position: settings.position,
    drawing: settings.drawing,
    layers,
    layerTree,
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
        preset: AtlasPreset(),
        options: {
          prefix: "prime",
          darkModeSelector: "light",
          cssLayer: false,
        },
      },
    })
    .use(ConfirmationService)
    .use(ToastService)
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
