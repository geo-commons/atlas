import "vite/modulepreload-polyfill";
import "tippy.js/dist/tippy.css";
import "es6-promise/auto";
import "whatwg-fetch";

import { createApp } from "vue";
import VueTippy from "vue-tippy";

import App from "./portal/App";
import PortalNotFound from "./portal/PortalNotFound.vue";
import { createRouter, createWebHistory } from "vue-router";
import { createPinia } from "pinia";
import { useGlobalStore } from "@/stores";
import PortalDashboard from "@/portal/pages/PortalDashboard.vue";
import PortalMapsPage from "@/portal/pages/PortalMapsPage.vue";
import PortalDatasetPage from "@/portal/pages/PortalDatasetsPage.vue";
import PortalDatasetDetailPage from "@/portal/pages/PortalDatasetDetailPage.vue";
import PortalTablesPage from "@/portal/pages/PortalTablesPage.vue";
import PortalSearchPage from "@/portal/pages/PortalSearchPage.vue";
import PrimeVue from "primevue/config";
import { AtlasPresetApp } from "@/utils/theme-preset";
import { ToastService } from "primevue";

const routes = [
  {
    path: "/",
    component: PortalDashboard,
    meta: {
      breadcrumb: "Home",
      menu: false,
    },
  },
  { path: "/maps", component: PortalMapsPage, meta: { breadcrumb: "Kaarten", menu: true } },
  { path: "/tables", component: PortalTablesPage, meta: { breadcrumb: "Tabellen", menu: true } },
  { path: "/search", component: PortalSearchPage, meta: { breadcrumb: "Zoeken", menu: true } },
  {
    path: "/datasets",
    component: PortalDatasetPage,
    meta: { breadcrumb: "Datasets", menu: true },
  },
  {
    path: "/datasets/:slug",
    name: "dataset-details",
    component: PortalDatasetDetailPage,
    meta: {
      breadcrumb: "Dataset details",
      menu: true,
      parentName: "Datasets",
    },
  },
  { path: "/:pathMatch(.*)*", name: "not-found", component: PortalNotFound },
];

const router = createRouter({
  history: createWebHistory(),
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
