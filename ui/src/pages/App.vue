<template>
  <div class="app">
    <header-menu v-if="!isEmbed && config.features.portal" />
    <map-renderer
      v-if="readyToRenderMap"
      :initial-position="position"
      :initial-layers="visibleLayers"
      :initial-draw-features="fetchedDrawFeatures"
      :user="user"
      :features="features"
      :config="config"
      :is-embed="isEmbed"
      :alert="alert"
      @position-changed="positionChanged"
      @layers-changed="layersChanged"
    />
  </div>
</template>

<script>
import Cookies from "js-cookie";
import GeoJSON from "ol/format/GeoJSON";
import nunjucks from "nunjucks";
import { register } from "ol/proj/proj4";
import { getDefinitions } from "@/utils/projections";
import HeaderMenu from "../components/HeaderMenu";
import MapRenderer from "@/components/MapRenderer/MapRenderer.vue";
import { mapState, mapStores } from "pinia";
import { useGlobalStore } from "@/stores"; // Register EPSG:28992 projection
import "primeicons/primeicons.css";

// Register EPSG:28992 projection
register(getDefinitions());

nunjucks.configure({ autoescaping: true });

export default {
  name: "App",
  components: {
    MapRenderer,
    HeaderMenu,
  },
  data() {
    return {
      readyToRenderMap: false,
      showInfoPanel: Boolean(this.position && this.position.marker),
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
      "drawing",
      "map",
    ]),
    visibleLayers() {
      if (this.map?.layers) {
        return this.layers
          .filter((layer) => this.map.layers.includes(layer.internal_id) || (layer.is_base && layer.is_visible))
          .map((layer) => {
            return {
              ...layer,
              is_visible: !layer.is_base ? true : layer.is_visible,
            };
          });
      }

      return this.layers;
    },
  },
  watch: {
    position: {
      handler(value) {
        // Toggle info panel based on if there is a marker present.
        this.showInfoPanel = Boolean(value.marker);
        this.pushHistoryState();
      },
      deep: true,
    },
    layers: {
      handler() {
        this.pushHistoryState();
      },
      deep: true,
    },
    drawing: {
      handler() {
        this.pushHistoryState();
      },
      deep: true,
    },
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
    };

    if (this.drawing) {
      this.fetchDrawing();
    }

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
    positionChanged(position) {
      this.globalStore.setPosition(position);
    },
    layersChanged(layers) {
      this.globalStore.setLayers(layers);
    },
    pushHistoryState() {
      const basePath = /(.*?)(@|$)/.exec(window.location.pathname);

      const x = encodeURIComponent(this.position.center[0].toFixed(2));
      const y = encodeURIComponent(this.position.center[1].toFixed(2));
      const zoom = encodeURIComponent(this.position.zoom);

      const layers = this.layers
        .filter((l) => l.is_visible && !l.is_base)
        .map((l) => l.id)
        .join(",");

      const baseLayer = this.layers.filter((l) => l.is_visible && l.is_base).map((l) => l.id);

      const markerCoords = this.position?.marker?.map((coord) => encodeURIComponent(coord.toFixed(2)));

      const urlParts = [
        `${basePath[1]}@${x},${y},${Math.round(zoom * 100) / 100}z`,
        `layers=${layers}`,
        `base=${baseLayer[0] || ""}`,
      ];

      if (this.drawing) {
        urlParts.push(`drawing=${this.drawing}`);
      }

      if (markerCoords?.length === 2) {
        urlParts.push(`marker=${markerCoords.join(",")}`);
      }

      window.history.replaceState({}, "", urlParts.join("/"));
    },
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
    async fetchDrawing() {
      const response = await fetch(`/atlas/api/v1/drawings/${this.drawing}/`);
      if (!response.ok) {
        return false;
      }

      const data = await response.json();

      const geojsonFormat = new GeoJSON();
      this.fetchedDrawFeatures = data.features.map((feature) => geojsonFormat.readFeature(feature));
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
