<template>
  <div class="content">
    <div class="header">
      <button
        v-tippy="{ placement: 'bottom' }"
        class="iconbutton __normal __outline"
        type="button"
        aria-label="Ga terug"
        content="Terug"
        @click="() => $emit('show-form')"
      >
        <ArrowLeftIcon class="icon" />
      </button>
      <h1>
        <LayerIcon class="icon" />
        Lagen
      </h1>
      <div class="header-spacer" />
    </div>

    <ul v-if="layers.length > 0" class="settings">
      <li v-for="layer in layers" :key="layer.id" class="setting">
        {{ layer.title }}
        <textarea
          :value="JSON.stringify(layer.client_style)"
          @change="(e) => (layer.client_style = JSON.parse(e.target.value))"
        />
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

<script>
import ArrowLeftIcon from "../../assets/icons/arrow-left-icon.svg";
import LayerIcon from "../../assets/icons/layer-icon.svg";
import AddLayerIcon from "../../assets/icons/add-layer-icon.svg";
import RemoveLayerIcon from "../../assets/icons/remove-layer-icon.svg";
import SearchIcon from "../../assets/icons/search-icon.svg";

export default {
  name: "MapLayers",
  components: { ArrowLeftIcon, LayerIcon, AddLayerIcon, RemoveLayerIcon, SearchIcon },
  props: {
    initialData: Object,
    layers: Array,
  },
  data() {
    return {
      allLayers: [],
      selectedLayers: [],
      searchQuery: "",
    };
  },
  computed: {
    unselectedLayers() {
      return this.allLayers.filter(
        (layer) => this.selectedLayers.filter((selectedLayer) => selectedLayer.id === layer.id).length === 0
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
    selectedLayerIds() {
      return this.selectedLayers.map((layer) => layer.id);
    },
  },
  async created() {
    await this.getLayers();

    if (this.initialData.layers) {
      this.selectedLayers = this.allLayers.filter((layer) => this.initialData.layers.includes(layer.id));
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

      this.$emit("change", this.selectedLayerIds);
    },
    deselectLayer(layerToDeselect) {
      this.selectedLayers = this.selectedLayers.filter((selectedLayer) => selectedLayer.id !== layerToDeselect.id);

      this.$emit("change", this.selectedLayerIds);
    },
  },
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: space-between;
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
</style>
