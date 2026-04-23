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
import PortalMetadatasetsPage from "@/portal/pages/PortalMetadatasetsPage.vue";
import PortalMetadatasetDetailPage from "@/portal/pages/PortalMetadatasetDetailPage.vue";
import PortalTablesPage from "@/portal/pages/PortalTablesPage.vue";
import PortalTableDetailPage from "@/portal/pages/PortalTableDetailPage.vue";
import PortalSearchPage from "@/portal/pages/PortalSearchPage.vue";
import PrimeVue from "primevue/config";
import { AtlasPreset } from "@/utils/theme-preset";
import { ToastService } from "primevue";
import { defineRule } from "vee-validate";
import { required } from "@vee-validate/rules";

defineRule("required", (value) => {
  if (!required(value)) {
    return "dit veld is verplicht";
  }
  return true;
});

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
  {
    path: "/tables/:slug",
    name: "table-details",
    component: PortalTableDetailPage,
    meta: {
      breadcrumb: "Tabel",
      menu: true,
      parentName: "Tabellen",
    },
  },
  { path: "/search", component: PortalSearchPage, meta: { breadcrumb: "Zoeken", menu: true } },
  {
    path: "/metadatasets",
    component: PortalMetadatasetsPage,
    meta: { breadcrumb: "Metadatasets", menu: true },
  },
  {
    path: "/metadatasets/:slug",
    name: "metadataset-details",
    component: PortalMetadatasetDetailPage,
    meta: {
      breadcrumb: "Metadataset details",
      menu: true,
      parentName: "Metadatasets",
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

  const { organization_primary_color, organization_text_color, organization_title_color } = data.config;

  // Note: darkModeSelector is set to "light" until we implement dark mode.
  const app = createApp(App)
    .use(PrimeVue, {
      theme: {
        preset: AtlasPreset(organization_primary_color, organization_title_color, organization_text_color),
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
