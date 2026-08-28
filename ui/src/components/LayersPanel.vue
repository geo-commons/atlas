<template>
  <div :class="{ 'show-compare-slider': showCompareSlider }">
    <div class="buttons-wrapper">
      <div
        class="buttons"
        :class="{
          isOpen: panel === 'layers' || panel === 'activeLayers',
          showSecondButton: !isEmbed && visibleLayers.length > 0,
        }"
      >
        <button
          v-if="!isEmbed"
          v-tippy
          class="iconbutton __map"
          :class="{ isActive: panel === 'layers' }"
          content="Alle lagen"
          aria-label="Toon alle lagen"
          :aria-expanded="String(panel === 'layers')"
          aria-controls="layers"
          @click="() => togglePanel('layers')"
        >
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
            <path d="M0 0h24v24H0V0z" fill="none" />
            <path
              fill="currentColor"
              d="M11.99 18.54l-7.37-5.73L3 14.07l9 7 9-7-1.63-1.27zM12 16l7.36-5.73L21 9l-9-7-9 7 1.63 1.27L12 16zm0-11.47L17.74 9 12 13.47 6.26 9 12 4.53z"
            />
          </svg>
        </button>

        <button
          v-if="visibleLayers.length > 0"
          v-tippy
          class="iconbutton __map"
          :tabindex="visibleLayers.length > 0 ? 0 : -1"
          :class="{ isActive: panel === 'activeLayers' }"
          content="Legenda"
          aria-label="Toon legenda"
          data-testid="toggle-visible-layers"
          :aria-expanded="String(panel === 'activeLayers')"
          aria-controls="visibleLayers"
          @click="() => togglePanel('activeLayers')"
        >
          <i class="pi pi-map" />
        </button>
      </div>

      <transition name="fade">
        <div v-if="!isEmbed && visibleLayers.length > 0" class="counter visible-layer-counter">
          {{ visibleLayers.length }}
        </div>
      </transition>
    </div>

    <transition name="fade">
      <ul v-if="panel === 'layers'" id="layers" class="layers">
        <div v-if="!showSearchBar" class="layers-search">
          <label for="layers-search">
            <svg xmlns="http://www.w3.org/2000/svg" height="18px" viewBox="0 0 24 24" width="18px" fill="currentColor">
              <path d="M0 0h24v24H0V0z" fill="none" />
              <path
                d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"
              />
            </svg>
          </label>
          <input
            id="layers-search"
            ref="searchLayerInput"
            v-model="searchQuery"
            type="search"
            name="query"
            placeholder="Zoek laag"
          />
        </div>
        <li v-if="!showSimpleLayerList">
          <ExpandButton
            v-for="category in categories"
            :key="category.id"
            :title="category.title"
            :is-open="debouncedSearchQuery != ''"
            class="category-wrapper"
          >
            <template #button>
              <div v-if="category.visibleLayerCount > 0" class="counter layer-counter">
                {{ category.visibleLayerCount }}
              </div>
            </template>
            <template #default>
              <ul :id="category.id" class="sublayers">
                <LayerListItem
                  v-for="layer in category.layers"
                  :key="layer.id"
                  :layer="layer"
                  :position="position"
                  :user="user"
                  :map-id="mapId"
                  @set-position="onSetPosition"
                  @on-fit="onFit"
                />
                <li v-for="subcategory in category.subcategories" :key="subcategory.id">
                  <ExpandButton :title="subcategory.title" :is-open="debouncedSearchQuery != ''" class="!-tw-ml-2.5">
                    <template #button>
                      <div v-if="subcategory.visibleLayerCount > 0" class="counter layer-counter">
                        {{ subcategory.visibleLayerCount }}
                      </div>
                    </template>
                    <template #default>
                      <ul :id="subcategory.id" class="sublayers subcategory-sublayers">
                        <LayerListItem
                          v-for="layer in subcategory.layers"
                          :key="layer.id"
                          :layer="layer"
                          :position="position"
                          :user="user"
                          :map-id="mapId"
                          @set-position="onSetPosition"
                          @on-fit="onFit"
                        />
                      </ul>
                    </template>
                  </ExpandButton>
                </li>
              </ul>
            </template>
          </ExpandButton>
        </li>
        <li v-if="showSimpleLayerList" :class="{ 'simple-layer-wrapper': panel === 'layers' }">
          <p>Beschikbare lagen</p>
          <div v-for="category in categories" :key="category.id">
            <ul :id="category.id" class="sublayers simple-sublayer">
              <LayerListItem
                v-for="layer in category.layers"
                :key="layer.id"
                :layer="layer"
                :position="position"
                :user="user"
                :map-id="mapId"
                @set-position="onSetPosition"
                @on-fit="onFit"
              />
              <div v-for="subcategory in category.subcategories" :key="subcategory.id">
                <LayerListItem
                  v-for="layer in subcategory.layers"
                  :key="layer.id"
                  :layer="layer"
                  :position="position"
                  :user="user"
                  :map-id="mapId"
                  @set-position="onSetPosition"
                  @on-fit="onFit"
                />
              </div>
            </ul>
          </div>
        </li>
      </ul>
    </transition>

    <transition name="fade">
      <ul v-if="visibleLayers.length > 0 && panel === 'activeLayers'" id="visibleLayers" class="visible-layers">
        <li v-if="showLegendToolbar" class="tool-bar">
          <div class="tw-flex tw-gap-1" :class="showToggleAllLayersInLegend ? 'tw-justify-between' : 'tw-justify-end'">
            <div v-if="showToggleAllLayersInLegend" class="tw-flex">
              <button
                v-tippy="{ placement: 'right' }"
                class="iconbutton __xs __round"
                content="Klap alle legenda's uit"
                aria-label="Klap alle legenda's uit"
                @click="openAllLayers"
              >
                <OpenAllIcon class="icon __smedium" />
              </button>
              <button
                v-tippy="{ placement: 'right' }"
                class="iconbutton __xs __round"
                content="Klap alle legenda's in"
                aria-label="Klap alle legenda's in"
                @click="closeAllLayers"
              >
                <CollapseAllIcon class="icon __smedium" />
              </button>
            </div>

            <button
              v-if="showSortLayersInLegendButton"
              v-tippy="{ placement: 'right' }"
              class="iconbutton __xs __round"
              :class="{ isActive: sortLayers }"
              :content="sortLayers ? 'Stop met volgorde aanpassen' : 'Pas kaartlaag volgorde aan'"
              :aria-label="sortLayers ? 'Stop met volgorde aanpassen' : 'Pas kaartlaag volgorde aan'"
              @click="onToggleSortLayers"
            >
              <SortIcon class="icon __smedium" />
            </button>
          </div>
        </li>
        <VisibleLayer
          v-for="(layer, i) in visibleLayers"
          :key="layer.id"
          :map-id="mapId"
          :position="position"
          :layer="layer"
          :layer-is-closable="!isEmbed"
          :layer-opacity-is-changable="!isEmbed"
          :is-open="layersOpen[layer.id] !== undefined ? layersOpen[layer.id] : i === 0"
          :user="user"
          :sort-layers="sortLayers"
          :index="i"
          :show-transparency-in-legend="showTransparencyInLegend"
          :show-not-selectable-in-legend="showNotSelectableInLegend"
          :show-information-in-legend="showInformationInLegend"
        />
      </ul>
    </transition>
  </div>
</template>

<script>
import ExpandButton from "./ExpandButton";
import VisibleLayer from "./VisibleLayer";
import LayerListItem from "./LayerListItem";
import CollapseAllIcon from "@/assets/icons/collapse-all-icon.svg";
import OpenAllIcon from "@/assets/icons/open-all-icon.svg";
import SortIcon from "@/assets/icons/sort-icon.svg";
import { mapState } from "pinia";
import { useDebounceFn } from "@vueuse/core";
import { useGlobalStore } from "@/stores";
import { useMapStore } from "@/stores/map_store";

export default {
  name: "LayersPanel",
  components: {
    CollapseAllIcon,
    OpenAllIcon,
    SortIcon,
    ExpandButton,
    VisibleLayer,
    LayerListItem,
  },
  props: {
    layers: Array,
    layerTree: {
      type: Array,
      default: () => [],
    },
    position: Object,
    user: Object,
    mapId: String,
    showSearchBar: Boolean,
    showSimpleLayerList: Boolean,
    showCompareSlider: Boolean,
    showToggleAllLayersInLegend: {
      type: Boolean,
      default: true,
    },
    showSortLayersInLegend: {
      type: Boolean,
      default: true,
    },
    showTransparencyInLegend: {
      type: Boolean,
      default: true,
    },
    showNotSelectableInLegend: {
      type: Boolean,
      default: true,
    },
    showInformationInLegend: {
      type: Boolean,
      default: true,
    },
    isEmbed: Boolean,
    layerPanelCollapsed: {
      type: Boolean,
      default: false,
    },
  },
  emits: ["set-position", "on-fit"],
  data() {
    return {
      panel: null,
      searchQuery: "",
      debouncedSearchQuery: "",
      updateDebouncedSearchQuery: null,
      mapStore: null,
      sortLayers: false,
      layersOpen: {},
    };
  },
  computed: {
    ...mapState(useGlobalStore, ["config"]),
    categories() {
      if (this.layerTree.length > 0) {
        return this.buildTreeCategories();
      }

      return [];
    },
    searchTerm() {
      return this.debouncedSearchQuery.trim().toLowerCase();
    },
    /**
     * Maps layer IDs to their full layer objects for quick lookup.
     * @returns {Map<string, Object>} A Map where the key is the layer ID and the value is the layer object.
     */
    layerById() {
      const layerById = new Map();

      (this.layers || []).forEach((layer) => {
        layerById.set(layer.id, layer);
      });

      return layerById;
    },
    /**
     * Stores precomputed searchable text per layer ID.
     * This avoids rebuilding the combined search string every time a layer is checked against the search term.
     * @returns {Map<string, string>} A Map where the key is the layer ID and the value is the combined searchable text for that layer.
     */
    searchableTextByLayerId() {
      const searchableTextByLayerId = new Map();

      (this.layers || []).forEach((layer) => {
        searchableTextByLayerId.set(layer.id, this.buildLayerSearchableText(layer));
      });

      return searchableTextByLayerId;
    },
    visibleLayers() {
      return this.mapStore ? this.mapStore.visibleLayers : [];
    },
    showSortLayersInLegendButton() {
      return this.config.features.sortLayer && this.showSortLayersInLegend;
    },
    showLegendToolbar() {
      return this.showToggleAllLayersInLegend || this.showSortLayersInLegendButton;
    },
  },
  watch: {
    searchQuery(newValue) {
      this.updateDebouncedSearchQuery(newValue);
    },
    showSortLayersInLegendButton(newValue) {
      if (!newValue) {
        this.sortLayers = false;
      }
    },
  },
  created() {
    this.updateDebouncedSearchQuery = useDebounceFn((value) => {
      this.debouncedSearchQuery = value;
    }, 150);
    this.mapStore = useMapStore(this.mapId);
    this.panel = this.layerPanelCollapsed ? null : this.mapStore.visibleLayers.length > 0 ? "activeLayers" : "layers";
  },
  mounted() {
    // Initialize layersOpen with the first layer open
    if (this.visibleLayers.length > 0) {
      this.layersOpen[this.visibleLayers[0].id] = true;
    }
  },
  methods: {
    buildTreeCategories() {
      return this.layerTree
        .map((category) => {
          const layers = this.getTreeLayers(category.layers || []);
          const subcategories = (category.subcategories || [])
            .map((subcategory) => ({
              ...subcategory,
              layers: this.getTreeLayers(subcategory.layers || []),
            }))
            .filter((subcategory) => subcategory.layers.length > 0)
            .map((subcategory) => ({
              ...subcategory,
              visibleLayerCount: this.getVisibleLayerCount(subcategory),
            }));

          return {
            ...category,
            layers,
            subcategories,
            visibleLayerCount: this.getVisibleLayerCount({ layers, subcategories }),
          };
        })
        .filter((category) => category.layers.length > 0 || category.subcategories.length > 0);
    },
    getTreeLayers(treeLayers) {
      return treeLayers
        .map((treeLayer) => this.layerById.get(treeLayer.id))
        .filter((layer) => layer && this.layerMatchesSearch(layer));
    },
    getVisibleLayerCount(category) {
      const directVisibleLayers = category.layers.filter((layer) => layer.is_visible).length;
      const subcategoryVisibleLayers = (category.subcategories || []).reduce((total, subcategory) => {
        return total + subcategory.layers.filter((layer) => layer.is_visible).length;
      }, 0);

      return directVisibleLayers + subcategoryVisibleLayers;
    },
    layerMatchesSearch(layer) {
      if (!this.searchTerm) {
        return true;
      }

      return this.searchableTextByLayerId.get(layer.id)?.includes(this.searchTerm) || false;
    },
    /**
     * Builds the normalized text used for layer search matching.
     * It combines layer title, description, configured search terms, and metadata title, description (abstract) and keywords, skips empty values,
     * and lowercases the result so matching can be case-insensitive.
     */
    buildLayerSearchableText(layer) {
      return [
        layer.title,
        layer.description,
        ...(layer.search_terms || []),
        layer.metadataset?.title,
        layer.metadataset?.abstract,
        layer.metadataset?.keyword,
      ]
        .filter(Boolean)
        .join("\n")
        .toLowerCase();
    },
    togglePanel(selectedPanel) {
      if (this.panel === selectedPanel) {
        this.panel = "";
        return;
      }

      this.panel = selectedPanel;

      if (selectedPanel === "layers" && !this.showSearchBar) {
        this.$nextTick(() => {
          this.$refs.searchLayerInput?.focus();
        });
      }
    },
    onSetPosition(newPosition) {
      this.$emit("set-position", newPosition);
    },
    onFit(extent) {
      this.$emit("on-fit", extent);
    },
    onToggleSortLayers() {
      this.sortLayers = !this.sortLayers;
    },
    openAllLayers() {
      this.visibleLayers.forEach((layer) => {
        this.layersOpen[layer.id] = true;
      });
    },
    closeAllLayers() {
      this.visibleLayers.forEach((layer) => {
        this.layersOpen[layer.id] = false;
      });
    },
  },
};
</script>

<style scoped>
.buttons-wrapper {
  position: relative;
}

.buttons {
  display: flex;
  background: white;
  width: var(--width-button-large);
  overflow: hidden;
  border-radius: var(--radius-normal);
  box-shadow: var(--shadow-normal);
  transition:
    width 0.1s ease,
    border-radius 0.1s;
}

.buttons.isOpen {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.buttons.showSecondButton {
  width: calc(var(--width-button-large) * 2 + 1px);
}

.iconbutton.__map {
  position: relative;
  width: var(--width-button-large);
  height: var(--width-button-large);
}

.iconbutton.__map:not(:last-child) {
  box-sizing: content-box;
  border-right: 1px solid var(--color-grey-50);
}

.visible-layer-counter {
  position: absolute;
  top: 2px;
  left: calc(100% - 8px);
}

.layer-counter {
  margin: 7px 8px 0 4px;
}

.layers,
.visible-layers {
  position: absolute;
  bottom: var(--width-button-large);
  left: 0;
  max-height: calc((100 * var(--vh)) - ((var(--width-button-large) * 2) + (var(--padding-screen) * 3)));
  width: calc(var(--width-detail) - (var(--padding-screen) * 2));
  max-width: calc(100vw - (var(--padding-screen) * 3) - var(--width-button-normal));
  overflow-y: auto;
  background: white;
  border-radius: var(--radius-small);
  border-bottom-left-radius: 0;
  box-shadow: var(--shadow-normal);
}

.visible-layers {
  width: fit-content;
  min-width: 200px;
  max-width: calc(100vw - (var(--padding-screen) * 3) - var(--width-button-normal));
}

.layers-search {
  width: 100%;
  display: flex;
  height: var(--width-button-large);
  border-bottom: 1px solid var(--color-grey-50);
}

.layers-search label {
  flex-shrink: 0;
  width: 32px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  color: var(--color-icon-grey);
}

.layers-search input {
  flex-grow: 1;
  height: 100%;
}

.sublayers.simple-sublayer {
  padding: 0px 0px 0px 8px;
}

.category-wrapper:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-50);
}

.simple-layer-wrapper {
  padding: 8px 8px 8px 0px;
}

.simple-layer-wrapper p {
  margin-bottom: 4px;
  margin-top: 0;
  padding-left: 8px;
  font-weight: 500;
}

.sublayers {
  padding: 0 4px 4px 30px;
}

@media (max-width: 640px) {
  .show-compare-slider .layers,
  .show-compare-slider .visible-layers {
    bottom: calc(var(--width-button-large) + 60px);
    max-height: calc((100 * var(--vh)) - ((var(--width-button-large) * 2) + (var(--padding-screen) * 3)) - 60px);
  }
}

.tool-bar {
  border-bottom: 1px solid var(--color-grey-50);
  padding: 6px 0 6px 0;
}
</style>
