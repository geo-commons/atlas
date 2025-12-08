<template>
  <div class="app">
    <header-menu v-if="!isEmbed && config.features.portal" />
    <outdated-map-alert v-if="outdated_map_slug" :theme-slug="outdated_map_slug" />
    <map-renderer
      v-if="readyToRenderMap"
      :initial-position="position"
      :initial-layers="layers"
      :user="user"
      :features="features"
      :config="config"
      :is-embed="isEmbed"
      :alert="alert"
      :map-id="'primary'"
    />
  </div>
</template>

<script>
import Cookies from "js-cookie";
import nunjucks from "nunjucks";
import { register } from "ol/proj/proj4";
import { getDefinitions } from "@/utils/projections";
import HeaderMenu from "../components/HeaderMenu";
import MapRenderer from "@/components/MapRenderer/MapRenderer.vue";
import { mapState, mapStores } from "pinia";
import { useGlobalStore } from "@/stores"; // Register EPSG:28992 projection
import "primeicons/primeicons.css";
import OutdatedMapAlert from "@/components/OutdatedMapAlert.vue";

// Register EPSG:28992 projection
register(getDefinitions());

nunjucks.configure({ autoescaping: true });

export default {
  name: "App",
  components: {
    OutdatedMapAlert,
    MapRenderer,
    HeaderMenu,
  },
  data() {
    return {
      readyToRenderMap: false,
      fetchedDrawFeatures: [],
      highlightedFeatures: [],
      features: {},
    };
  },
  computed: {
    ...mapStores(useGlobalStore),
    ...mapState(useGlobalStore, [
      "isEmbed",
      "alert",
      "position",
      "layers",
      "tool",
      "user",
      "config",
      "selectedArea",
      "initiallyShowLayerList",
      "map",
      "outdated_map_slug",
    ]),
  },
  created() {
    this.features = {
      searchbar: true,
      datapanel: true,
      selectarea: true,
      scale: true,
      measure: true,
      morepanel: true,
      layerlist: true,
      legend: true,
      baselayer: true,
      gps: true,
      zoom: true,
      markerOnClick: true,
      draw: true,
      edit_layer_features: true,
      compareLayers: this.config.features.compareLayers,
      panoramaViewers: true,
    };

    if (!this.user) {
      this.readyToRenderMap = true;
      return;
    }

    this.fetchAccessToken();

    this.fetchInterval = setInterval(
      () => {
        this.fetchAccessToken();
      },
      1000 * 60 * 5,
    ); // every 5 minutes
  },
  methods: {
    async fetchAccessToken() {
      const response = await fetch("/atlas/api/v1/token", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (!response.ok) {
        this.readyToRenderMap = true;
        return false;
      }

      const data = await response.json();

      this.globalStore.setUser({ ...this.user, token: data.token });

      this.readyToRenderMap = true;
    },
  },
};
</script>

<style>
@import "../assets/styles/main.css";
</style>
<style scoped>
.app {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}
</style>
