<template>
  <SidePanel
    large
    :show-panel="showDataPanel"
    @toggle-full-side-panel="toggleFullScreen"
  >
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
          <close-icon-large />
        </button>
      </div>
    </template>

    <template #default>
      <div v-if="visibleLayers.length == 0" class="flex-center">
        <p>Selecteer eerst een laag om verder te gaan</p>
      </div>
      <DataPanelDetailView
        v-if="selectedLayerId != null"
        :layer="selectedLayer"
        :position="position"
        :selected-area="selectedArea"
        :query="query"
        :user="user"
        @set-position="(position) => setPosition(position)"
        @on-fit="(position) => onFit(position)"
        @show-layers="() => resetSelectedLayer()"
      />
      <div v-if="selectedLayerId == null">
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
import ArrowLeftIcon from "../icons/ArrowLeftIcon.vue";
import CloseIconLarge from "../icons/CloseIconLarge.vue";

const visibleSourceTypes = ["WMS_WFS", "WFS"];

export default {
  name: "DataPanel",
  components: {
    DataPanelDetailView,
    SidePanel,
    SelectButton,
    ArrowLeftIcon,
    CloseIconLarge,
  },
  props: {
    position: Object,
    layers: Array,
    showDataPanel: Boolean,
    selectedArea: Object,
    user: Object,
    fullSizeWindow: Boolean,
  },
  data() {
    return {
      selectedLayerId: null,
      query: "",
    };
  },
  computed: {
    visibleLayers() {
      return this.layers.filter(
        (layer) =>
          layer.is_visible &&
          !layer.is_base &&
          visibleSourceTypes.includes(layer.source_type)
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
    visibleLayers() {
      // Check if selected layer is still available in the visible layers.
      if (
        this.selectedLayerId &&
        this.visibleLayers?.length > 0 &&
        !this.visibleLayers.some((layer) => layer.id === this.selectedLayerId)
      ) {
        this.resetSelectedLayer();
      }
    },
  },
  methods: {
    toggleDataPanel() {
      this.$emit("toggle-data-panel");
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

.no-margin {
  margin: 0;
}

.iconbutton {
  width: var(--width-button-normal);
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
