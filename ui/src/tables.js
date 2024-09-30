import "vite/modulepreload-polyfill";
import "tippy.js/dist/tippy.css";
import "es6-promise/auto";
import "whatwg-fetch";

import { createApp } from "vue";
import { createRouter, createWebHistory } from "vue-router";
import VueTippy from "vue-tippy";

import App from "./tables/App";
import ListView from "./tables/pages/ListView";
import NotFound from "./tables/pages/NotFound";
import { createPinia } from "pinia";
import { useGlobalStore } from "@/stores";
import PrimeVue from "primevue/config";
import { AtlasPreset } from "@/utils/theme-preset";

const routes = [
  { path: "/:tableSlug", component: ListView },
  { path: "/:pathMatch(.*)*", name: "not-found", component: NotFound },
];

const router = createRouter({
  history: createWebHistory("/tables/#"),
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
        preset: AtlasPreset,
        options: {
          prefix: "prime",
          darkModeSelector: "light",
          cssLayer: false,
        },
      },
    })
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
