<template>
  <SidePanel :show-panel="showPanel">
    <template #search>
      <button
        v-tippy="{ placement: 'right' }"
        class="iconbutton close-button"
        type="button"
        content="Sluit paneel"
        aria-label="Sluit paneel"
        @click="closeInfoPanel"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="24"
          viewBox="0 0 24 24"
          width="24"
        >
          <path d="M0 0h24v24H0z" fill="none" />
          <path
            d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
          />
        </svg>
      </button>
      <div class="search-query">
        <h1>{{ searchQuery }}</h1>
      </div>
    </template>

    <template #default>
      <FeatureInfo
        v-for="visibleLayer in visibleLayers"
        :key="visibleLayer.id"
        :is-open="visibleLayers.length === 1"
        :layer="visibleLayer"
        :position="position"
        @show-selected-feature="onFeatureSelect"
      />
    </template>
  </SidePanel>
</template>

<script>
import SidePanel from "./SidePanel";
import FeatureInfo from "./FeatureInfo";
import GeoJSON from "ol/format/GeoJSON";
import { getFeatureCenterCoordinates } from "../utils/geometry-helpers";

export default {
  name: "PointInfoPanel",
  components: {
    SidePanel,
    FeatureInfo,
  },
  props: {
    position: Object,
    layers: Array,
    showPanel: Boolean,
  },
  computed: {
    visibleLayers() {
      return this.layers.filter(
        (layer) =>
          layer.is_visible && layer.show_in_detail_panel && !layer.is_base
      );
    },
    searchQuery: {
      get() {
        return this.$store.state.searchQuery;
      },
      set(value) {
        this.$store.commit("setSearchQuery", value);
      },
    },
  },
  methods: {
    closeInfoPanel() {
      this.searchQuery = "";
      this.$emit("set-position", { ...this.position, marker: null });
    },
    onFeatureSelect(feature) {
      const geometry = new GeoJSON().readFeature(feature).getGeometry();
      const geometryExtend = geometry.getExtent();
      const center = getFeatureCenterCoordinates(feature);

      this.$emit("on-fit", geometryExtend);

      this.$emit("set-position", {
        ...this.position,
        marker: center,
        center: center,
      });
    },
  },
};
</script>

<style scoped>
h1 {
  font-size: var(--font-size-normal);
}

.search-query {
  margin-left: 10px;
  margin-right: 10px;
}

.close-button {
  width: var(--width-button-large);
  height: var(--width-button-large);
  border-radius: var(--radius-normal);
  border: 1px solid var(--color-grey-60);
}
</style>
