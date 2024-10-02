import "vite/modulepreload-polyfill";
import "tippy.js/dist/tippy.css";
import "es6-promise/auto";
import "whatwg-fetch";

import { createApp } from "vue";
import PrimeVue from "primevue/config";
import VueTippy from "vue-tippy";
import { getSettingsFromPath } from "./utils/router";
import App from "./admin/App";
import AdminDashboard from "./admin/pages/AdminDashboard";
import LayerList from "./admin/pages/LayerList";
import LayerCreateUpdate from "./admin/pages/LayerCreateUpdate";
import MapList from "./admin/pages/MapList";
import MapCreateUpdate from "./admin/pages/MapCreateUpdate";
import SourceList from "./admin/pages/SourceList";
import SourceCreateUpdate from "./admin/pages/SourceCreateUpdate";
import UserList from "./admin/pages/UserList";
import NotFound from "./admin/pages/NotFound";
import detectKeyboard from "@/utils/detect-keyboard";
import CategoryList from "@/admin/pages/CategoryList.vue";
import CategoryCreateUpdate from "@/admin/pages/CategoryCreateUpdate.vue";
import AdminSortPage from "@/admin/pages/AdminSortPage.vue";
import UserCreateUpdate from "@/admin/pages/UserCreateUpdate.vue";
import GroupList from "@/admin/pages/GroupList.vue";
import GroupCreateUpdate from "@/admin/pages/GroupCreateUpdate.vue";
import { defineRule } from "vee-validate";
import { createRouter, createWebHistory } from "vue-router";
import { email, required } from "@vee-validate/rules";
import { createPinia } from "pinia";
import { useGlobalStore } from "@/stores";
import ThemeCreateUpdate from "@/admin/pages/ThemeCreateUpdate.vue";
import ThemeList from "@/admin/pages/ThemeList.vue";
import DatasetList from "@/admin/pages/DatasetList.vue";
import DatasetCreateUpdate from "@/admin/pages/DatasetCreateUpdate.vue";
import LogList from "@/admin/pages/LogList.vue";
import TableList from "@/admin/pages/TableList.vue";
import TableCreateUpdate from "@/admin/pages/TableCreateUpdate.vue";
import ViewerList from "@/admin/pages/ViewerList.vue";
import ViewerCreateUpdate from "@/admin/pages/ViewerCreateUpdate.vue";
import AuthorizationList from "@/admin/pages/AuthorizationList.vue";
import AuthorizationCreateUpdate from "@/admin/pages/AuthorizationCreateUpdate.vue";
import LogView from "@/admin/pages/LogView.vue";
import AdminConfigurationPage from "@/admin/pages/AdminConfigurationPage.vue";
import AdminGeneralInformationPage from "@/admin/pages/AdminGeneralInformationPage.vue";
import { AtlasPreset } from "@/utils/theme-preset";
import TestLayerList from "@/admin/pages/TestLayerList.vue";

defineRule("required", (value) => {
  if (!required(value)) {
    return "Dit veld is verplicht";
  }
  return true;
});

defineRule("email", (value) => {
  if (!email(value)) {
    return "Voer een geldig e-mailadres in";
  }
  return true;
});

defineRule("max", (value, [max]) => {
  if (value.length > max) {
    return "De ingevoerde waarde overschrijdt het maximaal aantal toegestane karakters.";
  }
  return true;
});

const routes = [
  {
    path: "/",
    component: AdminDashboard,
    meta: { title: "Dashboard", menu: true },
  },
  { path: "/configuration", component: AdminConfigurationPage, meta: { title: "Configuratie", menu: true } },
  { path: "/maps", component: MapList, meta: { title: "Kaarten", menu: true } },
  {
    path: "/maps/update/:id",
    component: MapCreateUpdate,
    meta: { title: "Kaarten", menu: false },
  },
  {
    path: "/sources",
    component: SourceList,
    meta: { title: "Bronnen", menu: true },
  },
  {
    path: "/sources/update/:id",
    component: SourceCreateUpdate,
    meta: { title: "Bron bewerken", menu: true, breadcrumb: { sources: { title: "Bronnen" } } },
  },
  {
    path: "/layers",
    component: LayerList,
    meta: { title: "Kaartlagen", menu: true },
  },
  {
    path: "/lagen",
    component: TestLayerList,
    meta: { title: "Kaartlagen", menu: true },
  },
  {
    path: "/layers/update/:id",
    component: LayerCreateUpdate,
    meta: { title: "Kaartlaag bewerken", menu: true, breadcrumb: { layers: { title: "Kaartlagen" } } },
  },
  {
    path: "/categories",
    component: CategoryList,
    meta: { title: "Categorieën", menu: true },
  },
  {
    path: "/categories/update/:id",
    component: CategoryCreateUpdate,
    meta: {
      title: "Categorie bewerken",
      menu: true,
      breadcrumb: { categories: { title: "Categorieën" } },
    },
  },
  {
    path: "/tables",
    component: TableList,
    meta: { title: "Tabellen", menu: true },
  },
  {
    path: "/tables/update/:id",
    component: TableCreateUpdate,
    meta: { title: "Tabel bewerken", menu: true, breadcrumb: { tables: { title: "Tabellen" } } },
  },
  {
    path: "/users",
    component: UserList,
    meta: { title: "Gebruikers", menu: true },
  },
  {
    path: "/users/update/:id",
    component: UserCreateUpdate,
    meta: { title: "Gebruiker bewerken", menu: true, breadcrumb: { users: { title: "Gebruikers" } } },
  },
  {
    path: "/groups",
    component: GroupList,
    meta: { title: "Groepen", menu: true },
  },
  {
    path: "/groups/update/:id",
    component: GroupCreateUpdate,
    meta: { title: "Groep bewerken", menu: true, breadcrumb: { groups: { title: "Groepen" } } },
  },
  {
    path: "/viewers",
    component: ViewerList,
    meta: { title: "Viewers", menu: true },
  },
  {
    path: "/viewers/update/:id",
    component: ViewerCreateUpdate,
    meta: { title: "Viewer bewerken", menu: true, breadcrumb: { viewers: { title: "Viewers" } } },
  },
  {
    path: "/logs",
    component: LogList,
    meta: { title: "Logs", menu: true },
  },
  {
    path: "/logs/:id",
    component: LogView,
    meta: { title: "Log Bewerken", menu: true, breadcrumb: { viewers: { title: "Logs" } } },
  },
  {
    path: "/authorizations",
    component: AuthorizationList,
    meta: { title: "Autorisaties", menu: true },
  },
  {
    path: "/authorizations/update/:id",
    component: AuthorizationCreateUpdate,
    meta: { title: "Autorisatie bewerken", menu: true, breadcrumb: { authorizations: { title: "Autorisaties" } } },
  },
  {
    path: "/themes",
    component: ThemeList,
    meta: { title: "Thema's", menu: true },
  },
  {
    path: "/themes/update/:id",
    component: ThemeCreateUpdate,
    meta: { title: "Thema bewerken", menu: true, breadcrumb: { themes: { title: "Thema's" } } },
  },
  {
    path: "/datasets",
    component: DatasetList,
    meta: { title: "Datasets", menu: true },
  },
  {
    path: "/datasets/update/:id",
    component: DatasetCreateUpdate,
    meta: { title: "Dataset Bewerken", menu: true, breadcrumb: { datasets: { title: "Datasets" } } },
  },
  {
    path: "/general-information",
    component: AdminGeneralInformationPage,
    meta: { title: "Algemene informatie", menu: true },
  },
  {
    path: "/:parentRoute/sort",
    name: "sort",
    props: true,
    component: AdminSortPage,
    meta: {
      title: "Sortering",
      menu: true,
      breadcrumb: {
        layers: { url: "/layers", title: "Kaartlagen" },
        categories: { url: "/categories", title: "Categorieën" },
      },
    },
  },
  { path: "/:pathMatch(.*)*", name: "not-found", component: NotFound },
];

const router = createRouter({
  history: createWebHistory("/atlas/admin/#"),
  routes: routes,
});

// Atlas v3
document.addEventListener("DOMContentLoaded", () => {
  const el = document.querySelector("#app");
  if (!el) {
    return;
  }

  const data = JSON.parse(document.querySelector("#app-data").innerHTML);
  const settings = getSettingsFromPath(data.config);

  const layers = data.layers.map((layer) =>
    settings.visibleLayers && settings.visibleLayers.includes(layer.id) ? { ...layer, is_visible: true } : layer,
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
    user: data.user,
  };

  const pinia = createPinia();

  new detectKeyboard();

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
      locale: {
        emptySearchMessage: "Geen resultaten gevonden",
        emptyFilterMessage: "Geen resultaten gevonden",
        emptyMessage: "Geen resultaten gevonden",
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
  piniaStore.setInitialState(initialState);

  app.mount("#app");
});
