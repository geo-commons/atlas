<template>
  <SidePanel :show-panel="showPanel">
    <template #search>
      <div class="info-panel-header">
        <div class="search-query">
          <h1 v-if="searchQuery.title">{{ searchQuery.title }}</h1>
          <div class="coordinate-wrapper">
            <h1 v-if="!searchQuery.title">{{ searchQuery.coordinates }}</h1>
            <h4 v-else>{{ searchQuery.coordinates }}</h4>
            <vue-tippy
              placement="bottom-right"
              theme="popover"
              trigger="click"
              :distance="8"
              :delay="[0, 0]"
              :a11y="false"
            >
              <template #trigger>
                <button class="iconbutton __round show-on-hover" aria-label="Toon meer informatie">
                  <marker-icon class="icon __small" />
                </button>
              </template>
              <div class="container">
                <div class="heading">
                  <h3 class="title">EPSG:4326 projectie (WSG84)</h3>
                </div>
                <div class="property">
                  {{ searchQuery.coordEPSG4326 }}
                </div>
              </div>
            </vue-tippy>
          </div>
        </div>
        <button
          v-tippy="{ placement: 'right' }"
          class="iconbutton __normal __outline"
          type="button"
          content="Sluit paneel"
          aria-label="Sluit paneel"
          @click="closeInfoPanel"
        >
          <close-icon class="icon" />
        </button>
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
import { getFeatureCenterCoordinates } from "@/utils/geometry-helpers";
import CloseIcon from "@/assets/icons/close-icon.svg";
import MarkerIcon from "@/assets/icons/marker-icon.svg";

export default {
  name: "PointInfoPanel",
  components: {
    MarkerIcon,
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
        this.$store.commit("setSearchQuery", { title: value, coordinates: null });
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
  margin-bottom: 2px;
  margin-top: 0;
}

h4 {
  margin: 0;
  font-weight: var(--font-weight-normal);
}

.search-query {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: flex-start;
  flex-grow: 1;
}

.coordinate-wrapper {
  display: flex;
  font-size: var(--font-size-small);
  align-items: center;
  gap: 4px;
}

.info-panel-header {
  display: flex;
  justify-content: space-between;
  width: 100%;
  margin-top: 0.67em;
}

@media (min-width: 576px) {
  .info-panel-header {
    margin-top: 0;
  }
}

.show-on-hover {
  display: none;
}

.search-query:hover .show-on-hover {
  display: flex;
}

.container {
  font-weight: normal;
  text-align: left;
}

.heading {
  padding: 10px 16px;
  text-align: center;
  border-bottom: 1px solid var(--color-grey-60);
}

.title {
  margin: 0 0 4px;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-normal);
}

.property {
  padding: 8px 0;
  display: flex;
  flex-direction: column;
  font-weight: var(--font-weight-normal);
}
</style>
