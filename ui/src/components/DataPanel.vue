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
        :map-id="mapId"
        :layer="selectedLayer"
        :position="position"
        :selected-area="selectedArea"
        :user="user"
        @set-position="(position) => setPosition(position)"
        @on-fit="(position) => onFit(position)"
        @show-layers="() => resetSelectedLayer()"
      />
      <div v-else>
        <Button
          v-if="countOfActiveFilters > 0"
          severity="secondary"
          outlined
          class="!tw-text-sm !tw-font-medium !tw-mb-4 !tw-mx-4 xl:!tw-mx-5"
          @click="deleteAllFilters"
          >Verwijder filters <TrashIcon class="icon __marker __smedium" />
        </Button>
        <ActionButton
          v-for="layer in visibleLayers"
          :id="layer.id"
          :key="layer.id"
          :map-id="mapId"
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
import ActionButton from "./ActionButton.vue";
import ArrowLeftIcon from "../assets/icons/arrow-left-icon.svg";
import CloseIcon from "../assets/icons/close-icon.svg";
import TrashIcon from "@/assets/icons/trash-icon.svg";
import { useMapStore } from "@/stores/map_store";

const visibleSourceTypes = ["WMS_WFS", "WFS"];

export default {
  name: "DataPanel",
  components: {
    DataPanelDetailView,
    SidePanel,
    ActionButton,
    ArrowLeftIcon,
    CloseIcon,
    TrashIcon,
  },
  props: {
    mapId: String,
    position: Object,
    layers: Array,
    showDataPanel: Boolean,
    selectedArea: Object,
    user: Object,
    fullSizeWindow: Boolean,
  },
  emits: ["toggle-data-panel", "set-position", "on-fit", "toggle-full-side-panel"],
  data() {
    return {
      selectedLayerId: null,
      store: null,
    };
  },
  computed: {
    countOfActiveFilters() {
      return this.store.getActiveLayersWithFilterCount;
    },
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
  created() {
    this.store = useMapStore(this.mapId);
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
    deleteAllFilters() {
      this.store.resetAllFilters();
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
