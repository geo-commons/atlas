<template>
  <div class="app" :style="computedStyle">
    <header-menu v-if="!isEmbed && config.features.portal" />
    <map-renderer
      v-if="readyToRenderMap"
      :initial-position="position"
      :initial-layers="visibleLayers"
      :initial-draw-features="drawFeatures"
      :drawing="drawing"
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
import { mapState } from "vuex";
import { getDefinitions } from "@/utils/projections";
import HeaderMenu from "../components/HeaderMenu";
import MapRenderer from "@/components/MapRenderer/MapRenderer.vue"; // Register EPSG:28992 projection

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
      computedStyle: { "--color-primary": "#0066FF" },
      drawFeatures: [],
      highlightedFeatures: [],
      features: {},
    };
  },
  computed: {
    ...mapState({
      isEmbed: (state) => state.isEmbed,
      alert: (state) => state.alert,
      position: (state) => state.position,
      layers: (state) => state.layers,
      tool: (state) => state.tool,
      user: (state) => state.user,
      config: (state) => state.config,
      selectedArea: (state) => state.selectedArea,
      initiallyShowLayerList: (state) => state.initiallyShowLayerList,
      drawing: (state) => state.drawing,
      map: (state) => state.map,
    }),
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

    this.fetchInterval = setInterval(() => {
      this.fetchAccessToken();
    }, 1000 * 60 * 5); // every 5 minutes
  },
  methods: {
    positionChanged(position) {
      this.$store.commit("setPosition", position);
    },
    layersChanged(layers) {
      this.$store.commit("setLayers", layers);
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

      window.history.replaceState(
        {},
        "",
        `${basePath[1]}@${x},${y},${Math.round(zoom * 100) / 100}z/layers=${layers}/base=${
          baseLayer.length > 0 ? baseLayer[0] : ""
        }/drawing=${this.drawing ? this.drawing : ""}`
      );
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
      this.$store.commit("setUser", {
        ...this.user,
        token: data.token,
      });

      this.readyToRenderMap = true;
    },
    async fetchDrawing() {
      const response = await fetch(`/atlas/api/v1/drawings/${this.drawing}/`);
      if (!response.ok) {
        return false;
      }

      const data = await response.json();

      const geojsonFormat = new GeoJSON();
      this.drawFeatures = data.features.map((feature) => geojsonFormat.readFeature(feature));
    },
  },
};
</script>

<!-- Include multiselect -->
<style src="vue-multiselect/dist/vue-multiselect.css" />
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
