<template>
  <SidePanel :show-panel="showPanel">
    <template #search>
      <div class="header-wrapper">
        <div class="search-query">
          <h1>{{ searchQuery }}</h1>
        </div>

        <button
          v-tippy="{ placement: 'right' }"
          class="iconbutton close-button"
          type="button"
          content="Sluit paneel"
          aria-label="Sluit paneel"
          @click="closeInfoPanel"
        >
          <CloseIcon />
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
        :selected-feature-id="selectedFeatureId"
        @show-selected-feature="onFeatureSelect"
      />
    </template>
  </SidePanel>
</template>

<script>
import SidePanel from "./SidePanel";
import FeatureInfo from "./FeatureInfo";
import CloseIcon from "../assets/icons/close-icon.svg";

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
  data() {
    return {
      selectedFeatureId: null,
    };
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
      this.$emit("select-feature", null, null);
    },
    onFeatureSelect(feature, layer) {
      this.selectedFeatureId = feature?.id;
      this.$emit("select-feature", feature, layer);
    },
  },
};
</script>

<style scoped>
.header-wrapper {
  display: flex;
  justify-content: space-between;
  width: 100%;
}

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
