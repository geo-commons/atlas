import "vite/modulepreload-polyfill";
import "tippy.js/dist/tippy.css";
import "es6-promise/auto";
import "whatwg-fetch";

import VueTippy from "vue-tippy";

import App from "./tables/App";
import { createAtlasInertiaApp } from "@/utils/inertia";
import ListView from "./tables/pages/ListView";
import TableNotFound from "./tables/TableNotFound.vue";
import { createPinia } from "pinia";
import { useGlobalStore } from "@/stores";
import PrimeVue from "primevue/config";
import { AtlasPreset } from "@/utils/theme-preset";
import { ToastService } from "primevue";

const pages = {
  "Tables/List": ListView,
  "Tables/NotFound": TableNotFound,
};

const resolve = (name) => {
  const page = pages[name] || TableNotFound;
  page.layout = App;
  return page;
};

createAtlasInertiaApp({
  resolve,
  setup({ app, pageProps: data }) {
    const pinia = createPinia();

    // Note: darkModeSelector is set to "light" until we implement dark mode.
    app
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
    piniaStore.setInitialState(data);
  },
});
