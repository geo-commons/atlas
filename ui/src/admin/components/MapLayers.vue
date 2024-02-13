<template>
  <div class="content">
    <div class="header">
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
        <span v-if="selectedLayer" class="layer-wrapper"
          ><ChevronRightIcon class="no-margin" /> {{ getLayerTitle(selectedLayer.layer) }}</span
        >
      </h1>
    </div>

    <div v-show="!toggleLayer">
      <ul v-if="selectedLayers.length > 0" class="settings">
        <li v-for="selectedLayer in selectedLayers" :key="selectedLayer.id" class="setting">
          <button
            type="button"
            class="button __chevron __no-hover layer-button"
            @click="toggleLayerSettings(selectedLayer)"
          >
            {{ selectedLayer.title }}
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
    <MapLayer v-if="toggleLayer && selectedLayer" :initial-layer-data="selectedLayer" />
  </div>
</template>

<script>
import ArrowLeftIcon from "../../assets/icons/arrow-left-icon.svg";
import LayerIcon from "../../assets/icons/layer-icon.svg";
import AddLayerIcon from "../../assets/icons/add-layer-icon.svg";
import RemoveLayerIcon from "../../assets/icons/remove-layer-icon.svg";
import SearchIcon from "../../assets/icons/search-icon.svg";
import ChevronRightIcon from "@/assets/icons/chevron-right-icon.svg";
import MapLayer from "@/admin/components/MapLayer.vue";

export default {
  name: "MapLayers",
  components: { MapLayer, ChevronRightIcon, ArrowLeftIcon, LayerIcon, AddLayerIcon, RemoveLayerIcon, SearchIcon },
  props: {
    initialData: Object,
  },
  data() {
    return {
      allLayers: [],
      selectedLayers: [],
      selectedLayerData: [],
      searchQuery: "",
      toggleLayer: false,
      selectedLayer: null,
    };
  },
  computed: {
    unselectedLayers() {
      return this.allLayers.filter(
        (layer) =>
          this.selectedLayers.filter((selectedLayer) => selectedLayer.id === layer.id).length === 0 &&
          !layer.is_base &&
          layer.category !== null
      );
    },
    visibleUnselectedLayers() {
      if (!this.searchQuery) {
        return this.unselectedLayers;
      }

      return this.unselectedLayers.filter(
        (layer) => layer.title.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1
      );
    },
  },
  async created() {
    await this.getLayers();

    if (this.initialData.layers) {
      this.selectedLayerData = this.initialData.layers;
      this.selectedLayers = this.selectedLayerData.map((layer) => {
        return this.allLayers.find((l) => l.id === layer.layer);
      });
    }
  },
  methods: {
    async getLayers() {
      const result = await fetch("/atlas/api/v1/layers/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch layers");
      }

      this.allLayers = await result.json();
    },
    selectLayer(layer) {
      this.selectedLayers.push(layer);
      // todo: op deze manier resetten we eigenlijk altijd de settings is dit wenselijk?
      this.selectedLayerData.push({ layer: layer.id, settings: { is_visible: true } });
      this.$emit("change", this.selectedLayerData);
    },
    deselectLayer(layer) {
      this.selectedLayers = this.selectedLayers.filter((selectedLayer) => selectedLayer.id !== layer.id);
      this.selectedLayerData = this.selectedLayerData.filter((selectedLayer) => selectedLayer.layer !== layer.id);
      this.$emit("change", this.selectedLayerData);
    },
    getLayerTitle(layerId) {
      const layer = this.allLayers.find((layer) => layer.id === layerId);
      return layer ? layer.title : "";
    },
    back() {
      if (this.toggleLayer) {
        this.toggleLayer = false;
        this.selectedLayer = null;
        return;
      }

      this.$emit("show-form");
    },
    toggleLayerSettings(selectedLayer) {
      this.selectedLayer = this.selectedLayerData.find((layer) => layer.layer === selectedLayer.id);
      this.toggleLayer = !this.toggleLayer;
    },
  },
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: start;
}

.layers-header {
  flex-grow: 1;
}

.layer-wrapper {
  display: flex;
  align-items: center;
}

.no-margin {
  margin: 0;
}

.header-spacer {
  width: 40px;
}

.settings {
  margin-top: 24px;
}

.settings + .settings {
  margin-top: 40px;
}

.setting .iconbutton {
  margin-left: auto;
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
</style>
