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
          content="Zichtbare lagen"
          aria-label="Toon zichtbare lagen"
          :aria-expanded="String(panel === 'activeLayers')"
          aria-controls="visibleLayers"
          @click="() => togglePanel('activeLayers')"
        >
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
            <path d="M0 0h24v24H0V0z" fill="none" />
            <path
              fill="currentColor"
              d="M12 6c3.79 0 7.17 2.13 8.82 5.5C19.17 14.87 15.79 17 12 17s-7.17-2.13-8.82-5.5C4.83 8.13 8.21 6 12 6m0-2C7 4 2.73 7.11 1 11.5 2.73 15.89 7 19 12 19s9.27-3.11 11-7.5C21.27 7.11 17 4 12 4zm0 5c1.38 0 2.5 1.12 2.5 2.5S13.38 14 12 14s-2.5-1.12-2.5-2.5S10.62 9 12 9m0-2c-2.48 0-4.5 2.02-4.5 4.5S9.52 16 12 16s4.5-2.02 4.5-4.5S14.48 7 12 7z"
            />
          </svg>
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
            :is-open="searchQuery != ''"
            class="category-wrapper"
          >
            <template #button>
              <div v-if="category.layers.filter((layer) => layer.is_visible).length > 0" class="counter layer-counter">
                {{ category.layers.filter((layer) => layer.is_visible).length }}
              </div>
            </template>
            <template #default>
              <ul :id="category.id" class="sublayers">
                <li v-for="layer in category.layers" :key="layer.id" class="sublayer">
                  <input
                    :id="layer.id"
                    type="checkbox"
                    :name="layer.id"
                    :checked="layer.is_visible"
                    :disabled="layer.is_disabled || (layer.login_required && (!user || !user.token))"
                    @click="() => onSelectLayer(layer)"
                  />
                  <label :for="layer.id">
                    {{ layer.title }}
                  </label>
                  <LayerAuthentication v-if="layer.login_required && (!user || !user.token)" />
                  <button
                    v-if="layer.zoom_min && position.zoom < layer.zoom_min"
                    v-tippy="{ placement: 'right' }"
                    class="zoom-button"
                    content="Zoom in om deze laag te bekijken"
                    aria-label="Zoom in om deze laag te bekijken"
                    @click="(e) => zoomToAndShow(e, layer.zoom_min, layer)"
                  >
                    <ZoomInIcon />
                  </button>
                  <button
                    v-if="layer.zoom_max && position.zoom > layer.zoom_max"
                    v-tippy="{ placement: 'right' }"
                    class="zoom-button"
                    content="Zoom uit om deze laag te bekijken"
                    aria-label="Zoom uit om deze laag te bekijken"
                    @click="(e) => zoomToAndShow(e, layer.zoom_max, layer)"
                  >
                    <ZoomOutIcon />
                  </button>
                  <LayerFit v-if="layer.extent" :layer="layer" @click="() => onFit(layer)" />
                  <LayerInfo :layer="layer" />
                </li>
              </ul>
            </template>
          </ExpandButton>
        </li>
        <li v-if="showSimpleLayerList" :class="{ 'simple-layer-wrapper': panel === 'layers' }">
          <p>Beschikbare lagen</p>
          <div v-for="category in categories" :key="category.id">
            <ul :id="category.id" class="sublayers simple-sublayer">
              <li v-for="layer in category.layers" :key="layer.id" class="sublayer">
                <input
                  :id="layer.id"
                  type="checkbox"
                  :name="layer.id"
                  :checked="layer.is_visible"
                  :disabled="layer.is_disabled || (layer.login_required && (!user || !user.token))"
                  @click="() => onSelectLayer(layer)"
                />
                <label :for="layer.id">
                  {{ layer.title }}
                  <LayerAuthentication v-if="layer.login_required && (!user || !user.token)" />
                </label>
                <LayerFit v-if="layer.extent" :layer="layer" @click="() => onFit(layer)" />
                <LayerInfo :layer="layer" />
              </li>
            </ul>
          </div>
        </li>
      </ul>
    </transition>

    <transition name="fade">
      <ul v-if="visibleLayers.length > 0 && panel === 'activeLayers'" id="visibleLayers" class="visible-layers">
        <li v-if="config.features.sortLayer" class="tool-bar">
          <div class="tw-flex tw-justify-between tw-gap-1">
            <div class="tw-flex">
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
        />
      </ul>
    </transition>
  </div>
</template>

<script>
import { toRaw } from "vue";
import { intersects } from "ol/extent";
import ExpandButton from "./ExpandButton";
import VisibleLayer from "./VisibleLayer";
import LayerAuthentication from "./LayerAuthentication";
import LayerFit from "./LayerFit";
import LayerInfo from "./LayerInfo";
import ZoomInIcon from "../assets/icons/zoom-in-icon.svg";
import ZoomOutIcon from "../assets/icons/zoom-out-icon.svg";
import CollapseAllIcon from "@/assets/icons/collapse-all-icon.svg";
import OpenAllIcon from "@/assets/icons/open-all-icon.svg";
import SortIcon from "@/assets/icons/sort-icon.svg";
import { mapState } from "pinia";
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
    LayerAuthentication,
    LayerFit,
    LayerInfo,
    ZoomInIcon,
    ZoomOutIcon,
  },
  props: {
    layers: Array,
    position: Object,
    user: Object,
    mapId: String,
    showSearchBar: Boolean,
    showSimpleLayerList: Boolean,
    showCompareSlider: Boolean,
    isEmbed: Boolean,
  },
  data() {
    return {
      panel: null,
      searchQuery: "",
      mapStore: null,
      sortLayers: false,
      layersOpen: {},
    };
  },
  computed: {
    ...mapState(useGlobalStore, ["config"]),
    categories() {
      let categories = [];

      this.layers.forEach((mutableLayer) => {
        // Create a non-reactive copy of the layer to avoid mutating props
        const layer = toRaw(mutableLayer);

        if (!layer.category) {
          return;
        }

        if (this.searchQuery) {
          const searchTerm = this.searchQuery.toLowerCase();

          // Check if layer matches search criteria in title, meta description or search terms
          const matchesTitle = layer.title.toLowerCase().includes(searchTerm);
          const matchesDescription = layer.metadata?.description?.toLowerCase().includes(searchTerm) || false;
          const matchesSearchTerms =
            layer.search_terms?.some((term) => term.toLowerCase().includes(searchTerm)) || false;

          if (!matchesTitle && !matchesDescription && !matchesSearchTerms) {
            return;
          }
        }

        const existingCategory = categories.find((c) => c.id === layer.category.id);

        layer.is_disabled = false;
        if (layer.zoom_min && this.position.zoom < layer.zoom_min) {
          layer.is_disabled = true;
        }

        if (layer.zoom_max && this.position.zoom > layer.zoom_max) {
          layer.is_disabled = true;
        }

        if (layer.extent && this.position.extent && !intersects(layer.extent, this.position.extent)) {
          layer.is_disabled = true;
        }

        if (existingCategory) {
          existingCategory.layers.push(layer);
          return;
        }

        const newCategory = {
          ...layer.category,
          layers: [layer],
        };

        categories.push(newCategory);
      });

      return categories;
    },
    visibleLayers() {
      return this.mapStore ? this.mapStore.visibleLayers : [];
    },
  },
  created() {
    this.mapStore = useMapStore(this.mapId);
    this.panel = this.mapStore.visibleLayers.length > 0 ? "activeLayers" : "layers";
  },
  mounted() {
    // Initialize layersOpen with the first layer open
    if (this.visibleLayers.length > 0) {
      this.layersOpen[this.visibleLayers[0].id] = true;
    }
  },
  methods: {
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
    onSelectLayer(selectedLayer) {
      this.mapStore.toggleLayer({ selectedLayerId: selectedLayer.id, is_visible: !selectedLayer.is_visible });
    },
    onFit(selectedLayer) {
      this.$emit("on-fit", selectedLayer.extent);
    },
    zoomToAndShow(e, zoom, selectedLayer) {
      e.stopPropagation();

      this.$emit("set-position", {
        ...this.position,
        zoom,
      });

      if (!selectedLayer.is_visible) {
        this.mapStore.toggleLayer({ selectedLayerId: selectedLayer.id, is_visible: true });
      }
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

.sublayer {
  position: relative;
  display: flex;
}

.sublayer > input {
  position: absolute;
  top: 5px;
  left: 0;
  width: 14px;
  height: 14px;
  margin: 0;
}

.sublayer > label {
  display: flex;
  position: relative;
  width: 100%;
  cursor: pointer;
  padding: 2px 0 2px 20px;
  user-select: none;
  word-break: break-word;
}

.sublayer > input:disabled + label {
  color: var(--color-grey-80);
}

.zoom-button {
  margin-left: 5px;
  opacity: 0;
}

.layer:hover .zoom-button,
.sublayer:hover .zoom-button,
.tippy-active > .zoom-button,
.keyboard-user .zoom-button:focus {
  opacity: 1;
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
