<template>
  <div class="app">
    <header-menu v-if="config.features.portal" />
    <map-renderer
      ref="map"
      :initial-position="position"
      :initial-layers="visibleLayers"
      :user="user"
      :features="map.features"
      :settings="map.settings"
      :config="config"
      @position-changed="positionChanged"
    />
  </div>
</template>

<script>
import HeaderMenu from "../components/HeaderMenu";
import MapRenderer from "../components/MapRenderer/MapRenderer";
import { mapState, mapStores } from "pinia";
import { useGlobalStore } from "@/stores";

export default {
  name: "App",
  components: {
    HeaderMenu,
    MapRenderer,
  },
  data() {
    return {
      user: null,
    };
  },
  computed: {
    ...mapStores(useGlobalStore),
    ...mapState(useGlobalStore, ["position", "layers", "config", "map"]),
    visibleLayers() {
      if (this.map.layers) {
        // Get base layers.
        let configuredLayers = this.layers
          .filter((layer) => layer.is_base && layer.is_visible)
          .map((layer) => {
            return {
              ...layer,
              is_visible: !layer.is_base ? true : layer.is_visible,
            };
          });

        // Get selected layers on map level including configured settings.
        this.map.layers.forEach((selectedLayer) => {
          const layer = this.layers.find((l) => l.internal_id === selectedLayer.layer);

          if (!selectedLayer.settings.customSettings) {
            configuredLayers.push({ ...layer });
          } else {
            configuredLayers.push({
              ...layer,
              is_visible: selectedLayer.settings.is_visible,
              opacity: selectedLayer.settings.opacity,
              zoom_min: selectedLayer.settings.zoom_min,
              zoom_max: selectedLayer.settings.zoom_max,
              display_properties: selectedLayer.settings.display_properties,
              search_fields: selectedLayer.settings.search_fields,
              server_style: selectedLayer.settings.server_style,
              client_style: selectedLayer.settings.client_style,
              friendly_fields: selectedLayer.settings.friendly_fields,
              templated_properties: selectedLayer.settings.templated_properties,
              linked_data: selectedLayer.settings.linked_data,
              templates: selectedLayer.settings.templates,
            });
          }
        });

        return configuredLayers;
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

      const layers = this.visibleLayers
        .filter((l) => !l.is_base)
        .map((l) => l.id)
        .join(",");

      const baseLayer = this.visibleLayers.filter((l) => l.is_base).map((l) => l.id);

      window.history.replaceState(
        {},
        "",
        `${basePath[1]}@${x},${y},${Math.round(zoom * 100) / 100}z/layers=${layers}/base=${
          baseLayer.length > 0 ? baseLayer[0] : ""
        }`,
      );
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
