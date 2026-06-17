import { createInertiaApp } from "@inertiajs/vue3";
import { createApp, h } from "vue";
import { RouterLink, useRoute, useRouter } from "@/utils/inertia-routing";

export const createAtlasInertiaApp = ({ resolve, setup }) =>
  createInertiaApp({
    http: {
      xsrfCookieName: "csrftoken",
      xsrfHeaderName: "X-CSRFToken",
    },
    resolve,
    setup({ el, App, props, plugin }) {
      const app = createApp({ render: () => h(App, props) });
      app.use(plugin);
      app.component("RouterLink", RouterLink);
      Object.defineProperty(app.config.globalProperties, "$route", { get: () => useRoute() });
      Object.defineProperty(app.config.globalProperties, "$router", { get: () => useRouter() });

      setup({
        app,
        pageProps: props.initialPage.props,
      });

      app.mount(el);
    },
  });
