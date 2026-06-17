import "vite/modulepreload-polyfill";
import "tippy.js/dist/tippy.css";
import "es6-promise/auto";
import "whatwg-fetch";

import VueTippy from "vue-tippy";

import App from "./portal/App";
import { createAtlasInertiaApp } from "@/utils/inertia";
import PortalNotFound from "./portal/PortalNotFound.vue";
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

const pages = {
  "Portal/Dashboard": PortalDashboard,
  "Portal/Maps": PortalMapsPage,
  "Portal/Tables": PortalTablesPage,
  "Portal/TableDetail": PortalTableDetailPage,
  "Portal/Search": PortalSearchPage,
  "Portal/Metadatasets": PortalMetadatasetsPage,
  "Portal/MetadatasetDetail": PortalMetadatasetDetailPage,
  "Portal/NotFound": PortalNotFound,
};

const resolve = (name) => {
  const page = pages[name] || PortalNotFound;
  page.layout = App;
  return page;
};

createAtlasInertiaApp({
  resolve,
  setup({ app, pageProps: data }) {
    const pinia = createPinia();

    const { organization_primary_color, organization_text_color, organization_title_color } = data.config;

    // Note: darkModeSelector is set to "light" until we implement dark mode.
    app
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
