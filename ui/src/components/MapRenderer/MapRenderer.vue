<template>
  <div
    class="map-container"
    :class="{ showInfoPanel: showInfoPanel, showDataPanel }"
  >
    <div class="renderer-container">
      <OpenLayersRenderer
        ref="map"
        class="renderer"
        :position="position"
        :layers="layers"
        :tool="tool"
        :selected-area="selectedArea"
        :highlighted-features="highlightedFeatures"
        :selected-features="selectedFeatures"
        :padding="[0, 0, 0, 0]"
        :user="user"
        :features="features"
        :filters="filters"
        @position-changed="setPosition"
        @tool-used="toolUsed"
        @features-selected="featuresSelected"
      />
    </div>
    <ListPanel
      v-if="showList && layers.length > 0"
      ref="listPanel"
      :layer="layers[1]"
      :title-template="settings.title"
      :short-description-template="settings.short_description"
      :filters="filters"
      @hidePanel="toggleList"
      @on-fit="(feature) => $refs.map.fit(feature, { maxZoom: 18 })"
    />
    <FilterPanel
      v-if="showFilters"
      ref="filterPanel"
      :layer="layers[1]"
      :facets="settings.facets"
      :filters="filters"
      :user="user"
      @hidePanel="toggleFilters"
      @update-filters="(value) => (filters = value)"
    />
    <PointInfoPanel
      v-if="!showPanoramaPanel && features.markerOnClick"
      :layers="layers"
      :position="position"
      :show-panel="!showDataPanel && showInfoPanel"
      :user="user"
      @set-position="setPosition"
    />
    <DetailPanel
      v-if="!showPanoramaPanel && !features.markerOnClick && features.detail"
      :show-panel="selectedFeatures.length > 0"
      :features="selectedFeatures"
      @features-selected="featuresSelected"
    />
    <DataPanel
      v-if="!isEmbed && !showPanoramaPanel"
      ref="dataPanel"
      :layers="layers"
      :position="position"
      :selected-area="selectedArea"
      :show-data-panel="showDataPanel"
      :user="user"
      @set-position="setPosition"
      @on-fit="(layer) => $refs.map.fit(layer, { maxZoom: 18 })"
      @toggle-data-panel="toggleDataPanel"
    />

    <div class="ui-container">
      <SearchPanel
        v-if="features.searchbar"
        :position="position"
        :layers="layers"
        @set-position="setPosition"
        @toggle-data-panel="toggleDataPanel"
      />

      <div class="toggle-buttons">
        <PrimaryButton
          v-if="features.list && !showList"
          size="large"
          label="Lijst"
          drop-shadow
          @click="toggleList"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            enable-background="new 0 0 24 24"
            height="24px"
            viewBox="0 0 24 24"
            width="24px"
            fill="#000000"
          >
            <rect fill="none" height="24" width="24" />
            <path
              d="M3,5v14h18V5H3z M7,7v2H5V7H7z M5,13v-2h2v2H5z M5,15h2v2H5V15z M19,17H9v-2h10V17z M19,13H9v-2h10V13z M19,9H9V7h10V9z"
            />
          </svg>
        </PrimaryButton>
        <PrimaryButton
          v-if="features.filters && !showFilters"
          size="large"
          label="Verfijn"
          drop-shadow
          @click="toggleFilters"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="24px"
            viewBox="0 0 24 24"
            width="24px"
            fill="#000000"
          >
            <path d="M0 0h24v24H0V0z" fill="none" />
            <path d="M10 18h4v-2h-4v2zM3 6v2h18V6H3zm3 7h12v-2H6v2z" />
          </svg>
        </PrimaryButton>
      </div>

      <div class="top-right-panels">
        <ToolsPanel
          :features="features"
          :tool="tool"
          @set-tool="setTool"
          @set-selected-area="setSelectedArea"
        />
      </div>
      <div class="bottom-left-panels">
        <LayersPanel
          v-if="features.layerlist || features.legend"
          :layers="layers"
          :position="position"
          :user="user"
          :is-embed="features.legend && !features.layerlist"
          @toggle-layer="toggleLayer"
          @set-layer-opacity="setLayerOpacity"
          @on-fit="(layer) => $refs.map.fit(layer)"
        />
      </div>
      <div class="bottom-right-panels">
        <GeoLocationButton v-if="features.gps" @set-position="setPosition" />
        <ZoomPanel
          v-if="features.zoom"
          :position="position"
          @set-position="setPosition"
        />
      </div>
    </div>
  </div>
</template>

<script>
const reverseGeocodingEndpoint =
  "https://api.pdok.nl/bzk/locatieserver/search/v3_1/reverse";

import GeoJSON from "ol/format/GeoJSON";
import TileWMS from "ol/source/TileWMS";
import View from "ol/View";
import OpenLayersRenderer from "./renderers/OpenLayers/OpenLayers";

import PrimaryButton from "../PrimaryButton";
import ListPanel from "../ListPanel";
import FilterPanel from "../FilterPanel";
import DataPanel from "../DataPanel";
import PointInfoPanel from "../PointInfoPanel";
import DetailPanel from "../DetailPanel";
import SearchPanel from "../SearchPanel";
import LayersPanel from "../LayersPanel";
import ToolsPanel from "../ToolsPanel";
import ZoomPanel from "../ZoomPanel";
import GeoLocationButton from "../GeoLocationButton";

export default {
  name: "MapRenderer",
  components: {
    PrimaryButton,
    SearchPanel,
    LayersPanel,
    DataPanel,
    PointInfoPanel,
    DetailPanel,
    ListPanel,
    FilterPanel,
    OpenLayersRenderer,
    ToolsPanel,
    ZoomPanel,
    GeoLocationButton,
  },
  props: {
    initialLayers: Array,
    initialPosition: Object,
    user: Object,
    features: {
      type: Object,
      default: () => {
        return {
          scale: true,
        };
      },
    },
    settings: {
      type: Object,
      default: () => {
        return {
          facets: [],
        };
      },
    },
    isEmbed: {
      type: Boolean,
      default: () => false,
    },
  },
  data() {
    return {
      layers: this.initialLayers,
      position: this.initialPosition,
      highlightedFeatures: [],
      selectedFeatures: [],
      tool: "",
      selectedArea: null,
      showDataPanel: false,
      showPanoramaPanel: false,
      showList: false,
      showFilters: false,
      filters: {},
    };
  },
  computed: {
    showInfoPanel() {
      return this.position.marker ? true : false;
    },
  },
  watch: {
    initialPosition(value) {
      this.position = value;
    },
    initialLayers(value) {
      this.layers = value;
    },
  },
  methods: {
    async setPosition(position) {
      this.position = position;
      this.$emit("position-changed", position);

      if (!position.marker) {
        return;
      }

      this.reverseGeocode(position);
      this.getFeatureInfo(position);
    },
    async reverseGeocode(position) {
      try {
        const result = await fetch(
          `${reverseGeocodingEndpoint}?X=${position.marker[0]}&Y=${position.marker[1]}&rows=1&distance=20`
        );
        const data = await result.json();

        if (!data.response.docs || data.response.docs.length === 0) {
          this.$store.commit(
            "setSearchQuery",
            `(${Math.round(position.marker[0] * 100) / 100},${
              Math.round(position.marker[1] * 100) / 100
            })`
          );
          return;
        }

        const object = data.response.docs[0];
        this.$store.commit("setSearchQuery", object.weergavenaam);
      } catch (e) {
        console.error(e);
      }
    },
    async getFeatureInfo(position) {
      this.highlightedFeatures = [];

      const visibleLayers = this.layers.filter(
        (layer) => layer.is_selectable && !layer.is_base && layer.is_visible
      );
      visibleLayers.forEach(async (layer) => {
        const wmsSource = new TileWMS({
          url: layer.url,
          servertype: layer.server_type,
          params: {
            LAYERS: layer.name,
            TILED: true,
          },
        });

        const view = new View({
          center: this.position.center,
          zoom: this.position.zoom,
        });

        const url = wmsSource.getFeatureInfoUrl(
          position.marker,
          view.getResolution(),
          "EPSG:28992",
          {
            info_format: "application/json",
            feature_count: 20,
          }
        );

        try {
          const result = await fetch(url);
          const data = await result.json();
          this.highlightedFeatures = [
            ...this.highlightedFeatures,
            ...data.features.map((feature) =>
              new GeoJSON().readFeature(feature)
            ),
          ];
        } catch (e) {
          console.error(e);
        }
      });
    },
    toggleDataPanel() {
      this.showDataPanel = !this.showDataPanel;

      if (!this.showDataPanel) {
        this.selectedArea = null;
      }
    },
    toggleList() {
      this.showList = !this.showList;
    },
    toggleFilters() {
      this.showFilters = !this.showFilters;
    },
    setTool(tool) {
      this.tool = tool;
    },
    toolUsed(result) {
      if (result && result.sketch) {
        this.selectedArea = result.sketch.getGeometry();
      }

      switch (result.tool) {
        case "SELECT_POLYGON":
          this.showDataPanel = true;
          break;
      }
    },
    featuresSelected(selectedFeatures) {
      this.selectedFeatures = selectedFeatures;
    },
    setSelectedArea(selectedArea) {
      this.selectedArea = selectedArea;
    },
    toggleLayer([layerId, isVisible]) {
      this.layers = this.layers.map((layer) =>
        layer.id == layerId ? { ...layer, is_visible: isVisible } : layer
      );
    },
    setLayerOpacity([layerId, opacity]) {
      this.layers = this.layers.map((layer) =>
        layer.id == layerId ? { ...layer, opacity: opacity } : layer
      );
    },
  },
};
</script>

<style>
.tippy-tooltip {
  padding: 0;
  border-radius: var(--radius-normal);
  font-family: inherit;
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-bold);
  letter-spacing: 0em;
}

.tippy-tooltip .tippy-content {
  padding: 3px 7px 4px;
}

.tippy-tooltip.dark-theme .tippy-backdrop {
  background-color: var(--color-tooltip-dark);
}

.tippy-tooltip.primary-theme .tippy-backdrop {
  /* TODO: var(--color-primary) doesn't work */
  background-color: #0066ff;
}

.tippy-tooltip.popover-theme .tippy-backdrop {
  /* TODO: var(--color-primary) doesn't work */
  background-color: white;
}

.tippy-tooltip.popover-theme {
  background-color: white;
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-normal);
  color: #000000;
  letter-spacing: inherit;
  box-shadow: var(--shadow-normal);
}

.tippy-tooltip.popover-theme[x-placement^="left"] .tippy-arrow {
  border-left-color: white;
}

.tippy-tooltip.popover-theme[x-placement^="right"] .tippy-arrow {
  border-right-color: white;
}

.tippy-tooltip.popover-theme .tippy-content {
  padding: 0;
  overflow: auto;
}
</style>

<style scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
}

.renderer-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-flow: column;
}

@media (max-width: 575px) {
  .ui-container {
    order: -1;
  }
}

.ui-container {
  z-index: 1;
  flex-grow: 1;
  height: 100%;
  position: relative;
  pointer-events: none;
}

.ui-container > * {
  pointer-events: auto;
}

.map {
  flex: 1 1 auto;
  height: 0; /* fixes incorrect display of .ol-viewport on Safari 13.1 */
}

.top-right-panels {
  z-index: 1;
  position: absolute;
  top: var(--padding-screen);
  right: var(--padding-screen);
}

.bottom-left-panels {
  z-index: 1;
  position: absolute;
  bottom: var(--padding-screen);
  left: var(--padding-screen);
}

.bottom-right-panels {
  z-index: 1;
  position: absolute;
  bottom: var(--padding-screen);
  right: var(--padding-screen);
  display: flex;
  flex-direction: column;
}

.bottom-right-panels > *:not(:last-child) {
  margin-bottom: 12px;
}

.toggle-buttons {
  position: absolute;
  top: var(--padding-screen);
  left: var(--padding-screen);
  display: flex;
}

.toggle-buttons > *:not(:last-child) {
  margin-right: 8px;
}
</style>
