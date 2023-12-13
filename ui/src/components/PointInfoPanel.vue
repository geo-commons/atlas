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
        <close-icon />
      </button>
      <div class="search-query">
        <h1>{{ searchQuery }}</h1>
      </div>
    </template>

    <template #default>
      <FeatureInfo
        v-for="visibleLayer in visibleLayers"
        :key="visibleLayer.id"
        :is-open="true"
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
import CloseIcon from "@/assets/icons/close-icon.svg";

export default {
  name: "PointInfoPanel",
  components: {
    CloseIcon,
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
      return this.layers.filter((layer) => layer.is_visible && layer.show_in_detail_panel && !layer.is_base);
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
