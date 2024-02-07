import "tippy.js/themes/light-border.css";
import "es6-promise/auto";
import "whatwg-fetch";

import Vue from "vue";
import Vuex from "vuex";
import VueRouter from "vue-router";
import VueTippy from "vue-tippy";
// import { extend } from "vee-validate";

import { createStore } from "./store";
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
// import { email, max, required } from "vee-validate/dist/rules";

Vue.config.productionTip = false;

Vue.use(Vuex);
Vue.use(VueRouter);
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
Vue.component("VueTippy", VueTippy);

// extend("required", {
//   ...required,
//   message: "Dit veld is verplicht",
// });
//
// extend("email", {
//   ...email,
//   message: "Voer een geldig e-mailadres in",
// });
//
// extend("max", {
//   ...max,
//   message: "De ingevoerde waarde overschrijdt het maximaal aantal toegestane karakters.",
// });

const routes = [
  {
    path: "/",
    component: AdminDashboard,
    meta: { title: "Dashboard", menu: true },
  },
  { path: "/maps", component: MapList, meta: { title: "Kaarten", menu: true } },
  {
    path: "/maps/create",
    component: MapCreateUpdate,
    meta: { title: "Kaarten", menu: false },
  },
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
    path: "/sources/create",
    component: SourceCreateUpdate,
    meta: { title: "Bronnen", menu: true },
  },
  {
    path: "/sources/update/:id",
    component: SourceCreateUpdate,
    meta: { title: "Bronnen", menu: true },
  },
  {
    path: "/layers",
    component: LayerList,
    meta: { title: "Kaartlagen", menu: true },
  },
  {
    path: "/layers/update/:id",
    component: LayerCreateUpdate,
    meta: { title: "Kaartlagen", menu: true },
  },
  {
    path: "/categories",
    component: CategoryList,
    meta: { title: "Categorieën", menu: true },
  },
  {
    path: "/categories/update/:id",
    component: CategoryCreateUpdate,
    meta: { title: "Categorieën", menu: true },
  },
  {
    path: "/users",
    component: UserList,
    meta: { title: "Gebruikers", menu: true },
  },
  {
    path: "/users/update/:id",
    component: UserCreateUpdate,
    meta: { title: "Gebruikers", menu: true },
  },
  {
    path: "/groups",
    component: GroupList,
    meta: { title: "Groepen", menu: true },
  },
  {
    path: "/groups/update/:id",
    component: GroupCreateUpdate,
    meta: { title: "Groepen", menu: true },
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
        layers: { url: "/layers", displayName: "Kaartlagen" },
        categories: { url: "/categories", displayName: "Categorieën" },
      },
    },
  },
  { path: "*", component: NotFound },
];

const router = new VueRouter({
  routes,
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
    settings.visibleLayers && settings.visibleLayers.includes(layer.id) ? { ...layer, is_visible: true } : layer
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

  const store = createStore(initialState);

  new detectKeyboard();

  Vue.prototype.$primaryColor = "#424bff";

  new Vue({
    router,
    store,
    el: "#app",
    render: (c) => c(App),
  });
});
