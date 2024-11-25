<template>
  <SidePanel initial-size-large :show-panel="showDataPanel" @toggle-full-side-panel="toggleFullScreen">
    <template #search>
      <div class="flexer" :class="{ 'full-window-padding': fullSizeWindow }">
        <div v-if="selectedLayerId != null" class="selected-layer-wrapper">
          <button
            v-tippy="{ placement: 'bottom' }"
            class="iconbutton __normal __outline"
            type="button"
            aria-label="Ga terug"
            content="Terug"
            @click="resetSelectedLayer()"
          >
            <ArrowLeftIcon />
          </button>
          <h2 class="no-margin">{{ selectedLayer.title }}</h2>
        </div>
        <div v-if="selectedLayerId == null" class="selected-layer-wrapper">
          <h2 class="no-margin">Zichtbare lagen</h2>
        </div>
        <button
          v-tippy
          class="iconbutton __normal __outline"
          type="button"
          content="Sluit paneel"
          aria-label="Sluit paneel"
          @click="toggleDataPanel"
        >
          <CloseIcon class="icon" />
        </button>
      </div>
    </template>

    <template #default>
      <div v-if="visibleLayers.length === 0" class="no-layer-wrapper">
        <p>Selecteer eerst een laag om verder te gaan</p>
      </div>
      <DataPanelDetailView
        v-if="selectedLayer"
        :layer="selectedLayer"
        :position="position"
        :selected-area="selectedArea"
        :query="query"
        :user="user"
        :filters="filter"
        @set-position="(position) => setPosition(position)"
        @on-fit="(position) => onFit(position)"
        @show-layers="() => resetSelectedLayer()"
        @update-filters="(value) => updateFilters(value)"
      />
      <div v-else>
        <SelectButton
          v-for="layer in visibleLayers"
          :id="layer.id"
          :key="layer.id"
          :title="layer.title"
          class="select-border"
          @select-item="(layerId) => showSelectedLayer(layerId)"
        />
      </div>
    </template>
  </SidePanel>
</template>

<script>
import DataPanelDetailView from "./DataPanelDetailView.vue";
import SidePanel from "./SidePanel";
import SelectButton from "./SelectButton.vue";
import ArrowLeftIcon from "../assets/icons/arrow-left-icon.svg";
import CloseIcon from "../assets/icons/close-icon.svg";

const visibleSourceTypes = ["WMS_WFS", "WFS"];

export default {
  name: "DataPanel",
  components: {
    DataPanelDetailView,
    SidePanel,
    SelectButton,
    ArrowLeftIcon,
    CloseIcon,
  },
  props: {
    position: Object,
    layers: Array,
    showDataPanel: Boolean,
    selectedArea: Object,
    user: Object,
    filters: Object,
    fullSizeWindow: Boolean,
  },
  emits: ["toggle-data-panel", "set-position", "on-fit", "toggle-full-side-panel", "update-filters"],
  data() {
    return {
      selectedLayerId: null,
      query: "",
      filter: this.filters,
    };
  },
  computed: {
    visibleLayers() {
      return this.layers.filter(
        (layer) =>
          layer.is_visible &&
          !layer.is_base &&
          layer.show_in_detail_panel &&
          visibleSourceTypes.includes(layer.source_type),
      );
    },
    selectedLayer() {
      if (this.selectedLayerId != null) {
        return this.visibleLayers.find((layer) => {
          return layer.id === this.selectedLayerId;
        });
      }

      return null;
    },
  },
  watch: {
    layers: {
      handler() {
        // Check if selected layer is still available in the visible layers.
        if (this.selectedLayerId && !this.visibleLayers.some((layer) => layer.id === this.selectedLayerId)) {
          this.resetSelectedLayer();
        }
      },
      deep: true,
    },
  },
  methods: {
    toggleDataPanel() {
      this.$emit("toggle-data-panel");
      // Reset filters and search values on toggle DataPanel
      this.updateFilters({});
    },
    setPosition(value) {
      this.$emit("set-position", value);
    },
    onFit(value) {
      this.$emit("on-fit", value);
    },
    toggleFullScreen() {
      this.$emit("toggle-full-side-panel");
    },
    showSelectedLayer(layerId) {
      this.selectedLayerId = layerId;
    },
    resetSelectedLayer() {
      this.selectedLayerId = null;
      this.$emit("update-filters", {});
    },
    updateFilters(value) {
      this.$emit("update-filters", value);
    },
  },
};
</script>

<style scoped>
.close-button {
  width: var(--width-button-large);
  height: var(--width-button-large);
  border-radius: var(--radius-normal);
  border: 1px solid var(--color-grey-60);
}

.flexer {
  display: flex;
  justify-content: flex-end;
  flex-grow: 1;
}

.no-layer-wrapper {
  padding: 0 var(--padding-screen);
}

.no-margin {
  margin: 0;
}

@media screen and (min-width: 800px) {
  .full-window-padding {
    padding-right: 18px;
  }
}

.select-border:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-50);
}

.selected-layer-wrapper {
  display: flex;
  gap: 20px;
  align-items: center;
  margin: 0 auto;
  width: 100%;
}
</style>
