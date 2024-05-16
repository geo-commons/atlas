import "tippy.js/dist/tippy.css";
import "es6-promise/auto";
import "whatwg-fetch";

import { createApp } from "vue";
import VueTippy from "vue-tippy";

import App from "./portal/App";
import IndexView from "./portal/pages/IndexView";
import NotFound from "./portal/pages/NotFound";
import { createRouter, createWebHistory } from "vue-router";
import { createPinia } from "pinia";
import { useGlobalStore } from "@/stores";

const routes = [
  { path: "/", component: IndexView },
  { path: "/:pathMatch(.*)*", name: "not-found", component: NotFound },
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

  const app = createApp(App)
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
