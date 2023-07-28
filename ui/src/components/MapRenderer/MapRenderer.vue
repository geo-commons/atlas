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
      :layer="getSelectedLayer(settings.listLayerId)"
      :title-template="settings.title"
      :short-description-template="settings.short_description"
      :filters="filters"
      @hidePanel="toggleList"
      @on-fit="(feature) => $refs.map.fit(feature, { maxZoom: 18 })"
    />
    <FilterPanel
      v-if="showFilters"
      ref="filterPanel"
      :layer="getSelectedLayer(settings.filterLayerId)"
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
      @on-fit="(feature) => $refs.map.fit(feature, { maxZoom: 18 })"
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
      :full-size-window="showDataPanelFullScreen"
      @set-position="setPosition"
      @on-fit="(layer) => $refs.map.fit(layer, { maxZoom: 18 })"
      @toggle-data-panel="toggleDataPanel"
      @toggle-full-side-panel="toggleDataPanelFullScreen"
    />

    <div
      v-show="!showDataPanel || !showDataPanelFullScreen"
      class="ui-container"
    >
      <div class="top-left-panels">
        <SearchPanel
          v-if="features.searchbar"
          :position="position"
          :layers="layers"
          :features="features"
          @set-position="setPosition"
          @toggle-data-panel="toggleDataPanel"
        />
        <div class="toggle-buttons">
          <div
            v-if="features.datapanel && !features.searchbar"
            class="datapanel-btn-wrapper"
          >
            <DataPanelButton
              :is-subcomponent="false"
              @show-data-panel="toggleDataPanel"
            />
          </div>
          <PrimaryButton
            v-if="features.list && !showList"
            size="large"
            label="Lijst"
            drop-shadow
            @click="toggleList"
          >
            <ListIcon />
          </PrimaryButton>
          <PrimaryButton
            v-if="features.filters && !showFilters"
            size="large"
            label="Verfijn"
            drop-shadow
            @click="toggleFilters"
          >
            <FilterListIcon />
          </PrimaryButton>
        </div>
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
import ListIcon from "@/icons/ListIcon.vue";

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
import FilterListIcon from "@/icons/FilterListIcon.vue";
import DataPanelButton from "../DataPanelButton.vue";

export default {
  name: "MapRenderer",
  components: {
    FilterListIcon,
    ListIcon,
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
    DataPanelButton,
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
      showDataPanelFullScreen: false,
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
    toggleDataPanelFullScreen() {
      this.showDataPanelFullScreen = !this.showDataPanelFullScreen;
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
        case "SELECT_AREA":
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
    getSelectedLayer(layerId) {
      if (layerId) {
        return this.layers.find((filter) => {
          return filter.id === layerId;
        });
      }

      return null;
    },
  },
};
</script>

<style>
@import "../../assets/styles/main.css";
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
  position: absolute;
  top: calc((var(--padding-screen) * 2) + var(--width-button-large));
  right: var(--padding-screen);
  display: flex;
}

.top-left-panels {
  position: absolute;
  left: 0;
  right: 0;
  padding: var(--padding-screen);
  padding-bottom: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

@media (min-width: 576px) {
  .showDataPanel .top-left-panels {
    display: none;
  }
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
  display: flex;
}

.toggle-buttons > *:not(:last-child) {
  margin-right: 8px;
}

.datapanel-btn-wrapper {
  display: flex;
  background: white;
  width: var(--width-button-large);
  overflow: hidden;
  border-radius: var(--radius-normal);
  box-shadow: var(--shadow-normal);
  transition: width 0.1s ease, border-radius 0.1s;
  height: var(--width-button-large);
}
</style>
