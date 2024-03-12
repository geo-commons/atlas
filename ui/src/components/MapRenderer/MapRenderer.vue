<template>
  <div ref="mapContainer" class="map-container" :class="{ showInfoPanel, showDataPanel }" :style="computedStyle">
    <div class="renderer-container">
      <PanoramaPanel
        class="panorama-panel"
        :position="position"
        :is-open="showPanoramaPanel"
        @toggle="togglePanoramaPanel"
      />
      <OpenLayersRenderer
        ref="map"
        class="renderer"
        :position="position"
        :layers="layers"
        :tool="tool"
        :selected-area="selectedArea"
        :highlighted-features="highlightedFeatures"
        :selected-features="selectedFeatures"
        :user="user"
        :padding="mapPadding"
        :features="features"
        :filters="filters"
        :draw-features="drawFeatures"
        :drawing="drawing"
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
      @on-fit="(feature) => $refs.map.fit(feature, { maxZoom: 19 })"
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
      @on-fit="(feature) => $refs.map.fit(feature, { maxZoom: 19 })"
      @expanded-info-panel="toggleInfoPanel"
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
      :filters="filters"
      :full-size-window="showDataPanelFullScreen"
      @set-position="setPosition"
      @on-fit="(layer) => $refs.map.fit(layer, { maxZoom: 19 })"
      @toggle-data-panel="toggleDataPanel"
      @toggle-full-side-panel="toggleDataPanelFullScreen"
      @update-filters="(value) => (filters = value)"
    />

    <div v-show="!showDataPanel || !showDataPanelFullScreen" class="ui-container">
      <div class="top-left-panels" :class="{ 'extra-padding': showInfoPanel || showDataPanel }">
        <SearchPanel
          v-if="features.searchbar"
          :position="position"
          :layers="layers"
          :features="features"
          @set-position="setPosition"
          @toggle-data-panel="toggleDataPanel"
        />
        <div class="toggle-buttons">
          <div v-if="features.datapanel && !features.searchbar" class="datapanel-btn-wrapper">
            <DataPanelButton :is-subcomponent="false" @show-data-panel="toggleDataPanel" />
          </div>
          <PrimaryButton v-if="features.list && !showList" size="large" label="Lijst" drop-shadow @click="toggleList">
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
          v-if="!isEmbed && !showPanoramaPanel"
          :features="features"
          :config="config"
          :draw-features="drawFeatures"
          :tool="tool"
          :user="user"
          @set-tool="setTool"
          @set-selected-area="setSelectedArea"
          @drawing-saved="drawingSaved"
          @clear-draw="() => (drawFeatures = [])"
        />
        <MorePanel
          v-if="features.morepanel && !isEmbed && !showPanoramaPanel"
          :user="user"
          :show-disclaimer="config.show_disclaimer"
          @toggle-modal="toggleModal"
        />
      </div>
      <div class="bottom-left-panels">
        <LayersPanel
          v-if="features.layerlist || features.legend"
          :layers="layers"
          :position="position"
          :user="user"
          :show-search-bar="features.layerlistsearch"
          :show-simple-layer-list="features.layerlistsimple"
          :is-embed="features.legend && !features.layerlist"
          @toggle-layer="toggleLayer"
          @set-layer-opacity="setLayerOpacity"
          @on-fit="(layer) => $refs.map.fit(layer)"
          @set-position="setPosition"
        />
      </div>
      <div class="bottom-right-panels">
        <div v-if="features.baselayer" class="bottom-right-buttons">
          <button
            v-tippy="{ placement: 'left' }"
            class="iconbutton"
            content="Basislagen"
            aria-label="Toon basislagen"
            :aria-expanded="showBaseLayersPanel.toString()"
            aria-controls="baseLayers"
            @click="toggleBaseLayersPanel"
          >
            <MapIcon />
          </button>
          <transition name="fade">
            <BaseLayersPanel v-if="showBaseLayersPanel" :layers="layers" @toggle-layer="toggleLayer" />
          </transition>
        </div>
        <div v-if="!isEmbed && (panoramaViewers.length > 0 || obliqueViewers.length > 0)" class="bottom-right-buttons">
          <div class="wrapper">
            <button
              v-if="panoramaViewers.length > 0"
              v-tippy="{ placement: 'left' }"
              class="iconbutton"
              content="Rondkijkfoto"
              aria-label="Toon rondkijkfoto"
              @click="togglePanoramaPanel"
            >
              <PanoramaIcon />
            </button>
            <a
              v-if="obliqueViewers.length > 0"
              v-tippy="{ placement: 'left' }"
              :href="obliqueViewerUrl"
              target="_blank"
              rel="nofollow"
              class="iconbutton"
              content="Obliekfoto"
              aria-label="Toon obliekfoto"
            >
              <ObliqueIcon />
            </a>
          </div>
        </div>
        <GeoLocationButton v-if="features.gps" @set-position="setPosition" />
        <ZoomPanel v-if="features.zoom" :position="position" @set-position="setPosition" />
      </div>
    </div>

    <transition name="fade">
      <div>
        <EmbedModal v-if="modal === 'embed'" :layers="layers" :position="position" @toggle-modal="toggleModal" />
        <PrintModal v-if="modal === 'print'" @toggle-modal="toggleModal" @print-map-to-pdf="printMapToPdf" />
        <DrawingModal
          v-if="modal === 'drawing'"
          :layers="layers"
          :position="position"
          :drawing="drawing"
          @toggle-modal="toggleModal"
        />
      </div>
    </transition>
    <AlertMessage :alert="alert" />
  </div>
</template>

<script>
import ListIcon from "@/icons/ListIcon.vue";
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
import { isMobile } from "@/utils/helpers";
import { transform } from "ol/proj";
import BaseLayersPanel from "@/components/BaseLayersPanel.vue";
import MapIcon from "../../assets/icons/map-icon.svg";
import PanoramaIcon from "../../assets/icons/panorama-icon.svg";
import ObliqueIcon from "../../assets/icons/oblique-icon.svg";
import MorePanel from "@/components/MorePanel.vue";
import PanoramaPanel from "@/components/PanoramaPanel.vue";
import nunjucks from "nunjucks";
import PrintModal from "@/components/PrintModal.vue";
import DrawingModal from "@/components/DrawingModal.vue";
import AlertMessage from "@/components/AlertMessage.vue";
import EmbedModal from "@/components/EmbedModal.vue";

const reverseGeocodingEndpoint = "https://api.pdok.nl/bzk/locatieserver/search/v3_1/reverse";

export default {
  name: "MapRenderer",
  components: {
    EmbedModal,
    AlertMessage,
    DrawingModal,
    PrintModal,
    PanoramaPanel,
    MorePanel,
    BaseLayersPanel,
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
    MapIcon,
    PanoramaIcon,
    ObliqueIcon,
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
    config: {
      type: Object,
      default: () => {
        return {
          viewers: [],
          features: {},
        };
      },
    },
    alert: String,
    initialDrawFeatures: Array,
    drawing: Object,
  },
  data() {
    return {
      layers: this.initialLayers,
      position: this.initialPosition,
      drawFeatures: [],
      highlightedFeatures: [],
      selectedFeatures: [],
      tool: "",
      selectedArea: null,
      showDataPanel: false,
      showDataPanelFullScreen: false,
      showBaseLayersPanel: false,
      showPanoramaPanel: false,
      showList: false,
      showFilters: false,
      filters: {},
      infoPanelExpanded: false,
      mapPadding: [0, 0, 0, 0],
      computedStyle: {},
      modal: "",
    };
  },
  computed: {
    showInfoPanel() {
      return this.position.marker ? true : false;
    },
    panoramaViewers() {
      return this.config.viewers.filter((v) => !v.is_oblique);
    },
    obliqueViewers() {
      return this.config.viewers.filter((v) => v.is_oblique);
    },
  },
  watch: {
    initialPosition: {
      handler(value) {
        this.position = value;
      },
      deep: true,
    },
    initialLayers: {
      handler(value) {
        this.layers = value;
      },
      deep: true,
    },
    initialDrawFeatures: {
      handler(value) {
        this.drawFeatures = value;
      },
      deep: true,
    },
  },
  mounted() {
    window.addEventListener("resize", this.onResizeWindow);
    this.setViewportHeight();
  },
  unmounted() {
    window.removeEventListener("resize", this.onResizeWindow);
  },
  methods: {
    onResizeWindow() {
      this.setViewportHeight();
    },
    setViewportHeight() {
      this.computedStyle["--vh"] = this.$refs.mapContainer.clientHeight / 100 + "px";
    },
    async setPosition(position) {
      this.position = position;
      this.$emit("position-changed", position);

      if (!position.marker) {
        this.highlightedFeatures = [];
        return;
      }

      this.setWindowInnerWidth();

      this.reverseGeocode(position);
      this.getFeatureInfo(position);
    },
    async reverseGeocode(position) {
      try {
        const result = await fetch(
          `${reverseGeocodingEndpoint}?X=${position.marker[0]}&Y=${position.marker[1]}&rows=1&distance=20`
        );
        const data = await result.json();

        const coordinates = `(${Math.round(position.marker[0] * 100) / 100}, ${
          Math.round(position.marker[1] * 100) / 100
        })`;

        const convertedPosition = transform([position.marker[0], position.marker[1]], "EPSG:28992", "EPSG:4326");
        const coordEPSG4326 = `(${Math.round(convertedPosition[1] * 1000) / 1000}, ${
          Math.round(convertedPosition[0] * 1000) / 1000
        })`;

        if (!data.response.docs || data.response.docs.length === 0) {
          this.$store.commit("setSearchQuery", { coordinates: coordinates, coordEPSG4326: coordEPSG4326 });
          return;
        }

        const object = data.response.docs[0];
        this.$store.commit("setSearchQuery", {
          title: object.weergavenaam,
          coordinates: coordinates,
          coordEPSG4326: coordEPSG4326,
        });
      } catch (e) {
        console.error(e);
      }
    },
    async getFeatureInfo(position) {
      this.highlightedFeatures = [];

      const visibleLayers = this.layers.filter((layer) => layer.is_selectable && !layer.is_base && layer.is_visible);
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

        const url = wmsSource.getFeatureInfoUrl(position.marker, view.getResolution(), "EPSG:28992", {
          info_format: "application/json",
          feature_count: 20,
        });

        try {
          const result = await fetch(url);
          const data = await result.json();
          this.highlightedFeatures = [
            ...this.highlightedFeatures,
            ...data.features.map((feature) => new GeoJSON().readFeature(feature)),
          ];
        } catch (e) {
          console.error(e);
        }
      });
    },
    obliqueViewerUrl: function () {
      if (this.obliqueViewers.length === 0) {
        return "";
      }

      if (!this.obliqueViewers[0].url) {
        return "";
      }

      const position = this.position.marker || this.position.center;

      const latlong = transform(position, "EPSG:28992", "EPSG:4326");

      const properties = {
        lat: latlong[1],
        lon: latlong[0],
        x: position[0],
        y: position[1],
      };

      return nunjucks.renderString(this.obliqueViewers[0].url, properties);
    },
    printMapToPdf(settings) {
      this.$refs.map.printToPdf(settings);
    },
    drawingSaved(id) {
      this.$store.commit("setDrawing", id);
      this.modal = "drawing";
    },
    toggleModal(modal) {
      this.modal = modal;
    },
    togglePanoramaPanel() {
      this.showBaseLayersPanel = false;
      this.showPanoramaPanel = !this.showPanoramaPanel;
    },
    toggleDataPanel() {
      this.showDataPanel = !this.showDataPanel;
      if (!this.showDataPanel) {
        this.selectedArea = null;
      }

      this.setWindowInnerWidth();
    },
    toggleDataPanelFullScreen() {
      this.showDataPanelFullScreen = !this.showDataPanelFullScreen;
      this.setWindowInnerWidth();
    },
    toggleInfoPanel(expandInfoPanel) {
      this.infoPanelExpanded = expandInfoPanel;
      this.setWindowInnerWidth();
    },
    setWindowInnerWidth() {
      // Do not adjust the inner window padding for mobile screens.
      if (isMobile()) {
        this.$set(this.mapPadding, 3, 0);
        return;
      }

      if (this.showDataPanel && !this.showDataPanelFullScreen) {
        this.$set(this.mapPadding, 3, window.innerWidth * 0.5);
        return;
      }

      if (this.showInfoPanel) {
        if (this.infoPanelExpanded) {
          this.$set(this.mapPadding, 3, window.innerWidth * 0.5);
          return;
        }

        this.$set(this.mapPadding, 3, window.innerWidth * 0.25);
        return;
      }

      // reset padding of the inner window.
      this.$set(this.mapPadding, 3, 0);
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
        case "MEASURE_AREA":
        case "MEASURE_LINE":
          this.$store.commit("setSelectedArea", result.sketch.getGeometry());
          break;
        case "SELECT_AREA":
          this.showDataPanel = true;
          this.$store.commit("setSelectedArea", result.sketch.getGeometry());
          break;
        case "DRAW_POINT":
        case "DRAW_LINE":
        case "DRAW_POLYGON":
        case "DRAW_LABEL":
          this.drawFeatures.push(result.sketch);
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
      this.layers = this.layers.map((layer) => (layer.id == layerId ? { ...layer, is_visible: isVisible } : layer));
      this.$emit("layers-changed", this.layers);
    },
    setLayerOpacity([layerId, opacity]) {
      this.layers = this.layers.map((layer) => (layer.id == layerId ? { ...layer, opacity: opacity } : layer));
      this.$emit("layers-changed", this.layers);
    },
    getSelectedLayer(layerId) {
      if (layerId) {
        return this.layers.find((filter) => {
          return filter.id === layerId;
        });
      }

      return null;
    },
    toggleBaseLayersPanel() {
      this.showPanoramaPanel = false;
      this.showBaseLayersPanel = !this.showBaseLayersPanel;
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

@media (max-width: 932px) {
  .map-container {
    flex-direction: column;
  }

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

/*
.map {
  flex: 1 1 auto;
  height: 0;  fixes incorrect display of .ol-viewport on Safari 13.1
}
*/

.bottom-left-panels {
  z-index: 1;
  position: absolute;
  bottom: var(--padding-screen);
  left: var(--padding-screen);
}

.top-right-panels {
  position: absolute;
  top: calc((var(--padding-screen) * 2) + var(--width-button-large));
  right: var(--padding-screen);
  display: flex;
  gap: 12px;
}

.top-left-panels {
  position: absolute;
  left: var(--padding-screen);
  top: var(--padding-screen);
  padding: 0;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

@media (min-width: 1024px) {
  .top-left-panels.extra-padding {
    left: calc(var(--padding-screen) * 2);
  }
}

@media (min-width: 576px) {
  .top-right-panels {
    top: var(--padding-screen);
  }
}

@media (max-width: 576px) {
  .top-left-panels {
    left: 0;
    top: 0;
    padding: var(--padding-screen);
    width: 100%;
  }
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
  top: calc(8px + var(--width-button-large));
  left: 0;
  display: flex;
}

@media (max-width: 576px) {
  .toggle-buttons {
    top: calc(var(--padding-screen) * 2 + var(--width-button-large));
    left: var(--padding-screen);
  }
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

.bottom-right-buttons {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  background: white;
  border-radius: var(--radius-normal);
  overflow: hidden;
  box-shadow: var(--shadow-normal);
  height: var(--width-button-normal);
  transition: height 0.1s ease, border-radius 0.1s;
  overflow: hidden;
}

.bottom-right-buttons .iconbutton {
  width: var(--width-button-normal);
  height: var(--width-button-normal);
}

.bottom-right-buttons .iconbutton:first-child {
  box-sizing: content-box;
  border-bottom: 1px solid var(--color-grey-50);
}
</style>
