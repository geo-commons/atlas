import "vite/modulepreload-polyfill";
import "tippy.js/dist/tippy.css";
import "es6-promise/auto";
import "whatwg-fetch";

import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import VueTippy from "vue-tippy";

import App from "./tables/App";
import ListView from "./tables/pages/ListView";
import TableNotFound from "./tables/TableNotFound.vue";
import { createPinia } from "pinia";
import { useGlobalStore } from "@/stores";
import PrimeVue from "primevue/config";
import { AtlasPresetApp } from "@/utils/theme-preset";
import { ToastService } from "primevue";

const routes = [
  { path: "/:tableSlug", component: ListView },
  { path: "/:pathMatch(.*)*", name: "not-found", component: TableNotFound },
];

const router = createRouter({
  history: createWebHistory("/tables/"),
  routes: routes,
});

document.addEventListener("DOMContentLoaded", () => {
  const el = document.querySelector("#app");
  if (!el) {
    return;
  }

  const data = JSON.parse(document.querySelector("#app-data").innerHTML);

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
    .use(ToastService)
    .use(pinia)
    .use(router)
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

  app.mount("#app");
});
