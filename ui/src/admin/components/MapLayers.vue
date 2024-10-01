<template>
  <AdminSidePanel :loading="loading">
    <template #header>
      <button
        v-tippy="{ placement: 'bottom' }"
        class="iconbutton __normal __outline"
        type="button"
        aria-label="Ga terug"
        content="Terug"
        @click="back()"
      >
        <ArrowLeftIcon class="icon" />
      </button>
      <h1 class="layers-header">
        <LayerIcon class="icon" />
        Lagen
      </h1>
    </template>
    <template #default>
      <div>
        <div class="selected-layer-header-wrapper">
          <label class="setting-label">
            <MapIcon />
            Basis lagen</label
          >
          <div v-if="hasMultipleBaseLayersVisible" class="base-layer-warning">
            Let op: er zijn twee basis lagen die standaard zichtbaar zijn
          </div>
        </div>
        <ul class="settings">
          <li v-for="selectedLayer in selectedBaseLayers" :key="selectedLayer.layer" class="setting">
            <button
              type="button"
              class="button __chevron __no-hover layer-button"
              @click="toggleLayerSettings(selectedLayer)"
            >
              <span>
                {{ selectedLayer.title }}
              </span>
              <ViewIcon
                v-if="isLayerVisible(selectedLayer)"
                v-tippy
                content="Standaard zichtbaar"
                class="icon __smedium reset-transform"
              />
              <ChevronRightIcon class="icon setting-chevron" />
            </button>
            <button
              v-tippy="{ placement: 'bottom' }"
              class="iconbutton __normal __transparent-bg __no-hover"
              type="button"
              aria-label="Verwijder laag"
              content="Verwijder"
              @click="deselectLayer(selectedLayer)"
            >
              <RemoveLayerIcon class="icon" />
            </button>
          </li>
        </ul>
        <div class="selected-layer-header-wrapper">
          <label class="setting-label">
            <LayerIcon class="icon" />
            Kaartlagen</label
          >
        </div>
        <ul class="settings">
          <li v-for="selectedLayer in selectedRegularLayers" :key="selectedLayer.layer" class="setting">
            <button
              type="button"
              class="button __chevron __no-hover layer-button"
              @click="toggleLayerSettings(selectedLayer)"
            >
              {{ selectedLayer.title }}
              <ViewIcon
                v-if="isLayerVisible(selectedLayer)"
                v-tippy
                content="Standaard zichtbaar"
                class="icon __smedium reset-transform"
              />
              <ChevronRightIcon class="icon setting-chevron" />
            </button>
            <button
              v-tippy="{ placement: 'bottom' }"
              class="iconbutton __normal __transparent-bg __no-hover"
              type="button"
              aria-label="Verwijder laag"
              content="Verwijder"
              @click="deselectLayer(selectedLayer)"
            >
              <RemoveLayerIcon class="icon" />
            </button>
          </li>
        </ul>

        <div class="settings">
          <div class="search-wrapper">
            <SearchIcon class="icon" />
            <input id="layers-search" v-model="searchQuery" type="search" name="query" placeholder="Zoek laag" />
          </div>

          <ul>
            <li v-for="layer in visibleUnselectedLayers" :key="layer.id" class="setting">
              {{ layer.title }}
              <button
                v-tippy="{ placement: 'bottom' }"
                class="iconbutton __normal __transparent-bg __no-hover"
                type="button"
                aria-label="Voeg laag toe"
                content="Voeg toe"
                @click="selectLayer(layer)"
              >
                <AddLayerIcon class="icon" />
              </button>
            </li>
          </ul>
        </div>
      </div>
    </template>
  </AdminSidePanel>
</template>

<script>
import ArrowLeftIcon from "../../assets/icons/arrow-left-icon.svg";
import LayerIcon from "../../assets/icons/layer-icon.svg";
import AddLayerIcon from "../../assets/icons/add-layer-icon.svg";
import RemoveLayerIcon from "../../assets/icons/remove-layer-icon.svg";
import SearchIcon from "../../assets/icons/search-icon.svg";
import ChevronRightIcon from "@/assets/icons/chevron-right-icon.svg";
import AdminSidePanel from "@/admin/components/AdminSidePanel.vue";
import MapIcon from "@/assets/icons/map-icon.svg";
import ViewIcon from "@/assets/icons/view-icon.svg";

export default {
  name: "MapLayers",
  components: {
    ViewIcon,
    MapIcon,
    AdminSidePanel,
    ChevronRightIcon,
    ArrowLeftIcon,
    LayerIcon,
    AddLayerIcon,
    RemoveLayerIcon,
    SearchIcon,
  },
  props: {
    initialData: Object,
  },
  data() {
    return {
      allLayers: [],
      selectedMapLayerConfigs: [],
      searchQuery: "",
      loading: false,
    };
  },
  computed: {
    unselectedLayers() {
      return this.allLayers.filter(
        (layer) =>
          this.selectedMapLayerConfigs.filter((selectedLayer) => selectedLayer.layer === layer.id).length === 0,
      );
    },
    visibleUnselectedLayers() {
      if (!this.searchQuery) {
        return this.unselectedLayers;
      }

      return this.unselectedLayers.filter(
        (layer) => layer.title.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1,
      );
    },
    selectedBaseLayers() {
      let baseLayers = [];

      this.selectedMapLayerConfigs.forEach((l) => {
        // get default layer settings
        const layerData = this.allLayers.find((layer) => layer.id === l.layer);

        if ((!l.settings.customSettings && layerData.is_base) || (l.settings.customSettings && l.settings.is_base)) {
          baseLayers.push(layerData);
        }
      });

      return baseLayers;
    },
    selectedRegularLayers() {
      let layers = [];

      this.selectedMapLayerConfigs.forEach((l) => {
        // get default layer settings
        const layerData = this.allLayers.find((layer) => layer.id === l.layer);

        if ((!l.settings.customSettings && !layerData.is_base) || (l.settings.customSettings && !l.settings.is_base)) {
          layers.push(layerData);
        }
      });

      return layers;
    },
    hasMultipleBaseLayersVisible() {
      return (
        this.selectedMapLayerConfigs.filter((l) => {
          // Check if the layer has custom settings.
          if (l.settings.customSettings && l.settings.is_base && l.settings.is_visible) {
            return l;
          }

          // When the layer has no custom settings get corresponding default layer settings.
          const layerData = this.allLayers.find((layer) => layer.id === l.layer);
          if (!l.settings.customSettings && layerData.is_base && layerData.is_visible) {
            return l;
          }
        }).length > 1
      );
    },
  },
  async created() {
    await this.getLayers();

    this.selectedMapLayerConfigs = this.initialData.layers;
  },
  methods: {
    async getLayers() {
      this.loading = true;
      const result = await fetch("/atlas/api/v1/layers/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch layers");
      }

      this.allLayers = await result.json();
      this.loading = false;
    },
    selectLayer(layer) {
      this.selectedMapLayerConfigs.push({
        layer: layer.id,
        settings: { customSettings: false },
      });
      this.$emit("update-layers", this.selectedMapLayerConfigs);
    },
    deselectLayer(layer) {
      this.selectedMapLayerConfigs = this.selectedMapLayerConfigs.filter(
        (selectedLayer) => selectedLayer.layer !== layer.id,
      );

      this.$emit("update-layers", this.selectedMapLayerConfigs);
    },
    back() {
      this.$emit("show-form");
    },
    toggleLayerSettings(selectedLayer) {
      this.$emit("show-layer", selectedLayer.id);
    },
    isLayerVisible(layer) {
      const layerConfig = this.selectedMapLayerConfigs.find((l) => l.layer === layer.id);

      if (layerConfig.settings.customSettings) {
        return layerConfig.settings.is_visible;
      }

      return layer.is_visible;
    },
  },
};
</script>

<style scoped>
.settings + .settings {
  margin-top: 40px;
}

.setting .iconbutton {
  margin-left: auto;
}

li.setting:first-child {
  border-top: none;
}

.selected-layer-header-wrapper {
  width: 100%;
  height: 54px;
  border-bottom: 1px solid var(--color-grey-60);
  display: flex;
  flex-direction: column;
  gap: 4px;
  align-items: center;
  justify-content: center;
}

.setting-label {
  display: flex;
  gap: 4px;
  align-items: center;
  justify-content: center;
  font-weight: var(--font-weight-bold);
}

.base-layer-warning {
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-small);
  color: var(--color-alert);
}

.search-wrapper {
  position: relative;
  border-top: 1px solid var(--color-grey-60);
  border-bottom: 1px solid var(--color-grey-60);
  margin-bottom: -1px;
}

.search-wrapper svg {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 16px;
  margin: auto 0;
  pointer-events: none;
}

.search-wrapper input {
  width: 100%;
  height: 48px;
  padding: 0 0 0 48px;
}

.setting-chevron {
  width: 32px;
  margin-left: auto;
}

.layer-button {
  background: transparent;
  padding: 0;
}

/* The hover transform somehow breaks v-tippy.  */
.button.__chevron:hover svg.reset-transform {
  transform: translateX(0);
}
</style>
