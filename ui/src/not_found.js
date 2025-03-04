import { createApp } from "vue";
import MapNotFound from "./map/MapNotFound.vue";

document.addEventListener("DOMContentLoaded", () => {
  const el = document.querySelector("#app");
  if (!el) {
    console.error("App element not found");
    return;
  }

  const app = createApp(MapNotFound);
  app.mount("#app");
});
