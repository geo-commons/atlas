<template>
  <div
    id="map-container"
    ref="mapContainer"
    class="map-container"
    :class="{ showInfoPanel, showDataPanel, portalHeader: !isEmbed && config.features.portal }"
    :style="computedStyle"
  >
    <div class="renderer-container">
      <Splitter
        v-if="!isEmbed && (panoramaViewers.length > 0 || obliqueViewers.length > 0)"
        ref="splitter"
        style="height: 100vh"
        layout="vertical"
      >
        <SplitterPanel v-if="showPanoramaPanel" class="flex items-center justify-center panorama-splitter">
          <PanoramaPanel
            class="panorama-panel"
            :position="position"
            @toggle="togglePanoramaPanel"
            @toggle-full-screen="togglePanoramaPanelFullScreen"
          />
        </SplitterPanel>
        <SplitterPanel v-if="!showPanoramaPanelFullScreen" class="flex items-center justify-center">
          <OpenLayersRenderer
            ref="map"
            class="renderer in-splitter"
            :position="position"
            :layers="layers"
            :tool="tool"
            :map-id="mapId"
            :selected-area="selectedArea"
            :highlighted-features="highlightedFeatures"
            :selected-features="selectedFeatures"
            :map-area="mapArea"
            :user="user"
            :config="config"
            :padding="mapPadding"
            :features="features"
            :draw-features="drawFeatures"
            :color="color"
            :stroke-width="strokeWidth"
            :font-size="fontSize"
            @position-changed="setPosition"
            @tool-used="toolUsed"
            @features-selected="featuresSelected"
            @on-fit="(position) => onFit(position, true)"
            @loading-print-to-pdf="setLoadingPrint"
          />
        </SplitterPanel>
      </Splitter>
      <OpenLayersRenderer
        v-else
        ref="map"
        class="renderer in-splitter"
        :position="position"
        :layers="layers"
        :tool="tool"
        :map-id="mapId"
        :selected-area="selectedArea"
        :highlighted-features="highlightedFeatures"
        :selected-features="selectedFeatures"
        :map-area="mapArea"
        :user="user"
        :config="config"
        :padding="mapPadding"
        :features="features"
        :draw-features="drawFeatures"
        :color="color"
        :stroke-width="strokeWidth"
        :font-size="fontSize"
        @position-changed="setPosition"
        @tool-used="toolUsed"
        @features-selected="featuresSelected"
        @on-fit="(position) => onFit(position, true)"
        @loading-print-to-pdf="setLoadingPrint"
      />
    </div>
    <ListPanel
      v-if="showList && layers.length > 0"
      ref="listPanel"
      :map-id="mapId"
      :layer="getSelectedLayer(settings.listLayerId)"
      :title-template="settings.title"
      :short-description-template="settings.short_description"
      @hidePanel="toggleList"
      @on-fit="(feature) => $refs.map.fit(feature, { maxZoom: 19 })"
    />
    <FilterPanel
      v-if="showFilters"
      ref="filterPanel"
      :layer="getSelectedLayer(settings.filterLayerId)"
      :facets="settings.facets"
      :user="user"
      :map-id="mapId"
      @hidePanel="toggleFilters"
    />
    <PointInfoPanel
      v-if="!showPanoramaPanel && features.markerOnClick"
      :layers="layers"
      :position="position"
      :show-panel="!showDataPanel && showInfoPanel"
      :user="user"
      @set-position="setPosition"
      @on-fit="(feature) => $refs.map.fit(feature, { maxZoom: 19, duration: 1000 })"
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
      :selected-area="selectedAreaDataPanel"
      :show-data-panel="showDataPanel"
      :user="user"
      :map-id="mapId"
      :full-size-window="showDataPanelFullScreen"
      @set-position="setPosition"
      @on-fit="(layer) => $refs.map.fit(layer, { maxZoom: 19, duration: 1000 })"
      @toggle-data-panel="toggleDataPanel"
      @toggle-full-side-panel="toggleDataPanelFullScreen"
    />

    <div v-show="!showDataPanel || !showDataPanelFullScreen" class="ui-container">
      <div class="top-left-panels" :class="{ 'extra-padding': showInfoPanel || showDataPanel }">
        <SearchPanel
          v-if="features.searchbar"
          :position="position"
          :layers="layers"
          :features="features"
          :map-id="mapId"
          :show-data-panel="showDataPanel"
          @set-position="setPosition"
          @toggle-data-panel="toggleDataPanel"
        />
        <div class="toggle-buttons" :class="{ 'position-top': !features.searchbar }">
          <div v-if="features.datapanel && !features.searchbar" class="datapanel-btn-wrapper">
            <DataPanelButton
              :is-subcomponent="false"
              :show-data-panel="showDataPanel"
              :map-id="mapId"
              @show-data-panel="toggleDataPanel"
            />
          </div>
          <PrimaryButton
            v-if="features.list && !showList"
            size="large"
            label="Lijst"
            drop-shadow
            @on-button-click="toggleList"
          >
            <ListIcon />
          </PrimaryButton>
          <PrimaryButton
            v-if="features.filters && !showFilters"
            size="large"
            label="Verfijn"
            drop-shadow
            @on-button-click="toggleFilters"
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
          :removed-draw-features="removedDrawFeatures"
          :tool="tool"
          :user="user"
          :color="color"
          :stroke-width="strokeWidth"
          :font-size="fontSize"
          @set-tool="setTool"
          @set-selected-area="setSelectedArea"
          @drawing-saved="drawingSaved"
          @clear-draw="() => (drawFeatures = [])"
          @setInteraction="setInteraction"
          @setColor="setColor"
          @setStrokeWidth="setStrokeWidth"
          @setFontSize="setFontSize"
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
          :layers="regularLayers"
          :position="position"
          :user="user"
          :map-id="mapId"
          :show-search-bar="features.layerlistsearch"
          :show-simple-layer-list="features.layerlistsimple"
          :is-embed="features.legend && !features.layerlist"
          @toggle-layer="toggleLayer"
          @set-layer-opacity="setLayerOpacity"
          @on-fit="(layer) => $refs.map.fit(layer)"
          @set-position="setPosition"
          @toggle-is-selectable="onToggleIsSelectable"
        />
      </div>
      <div class="bottom-right-panels">
        <div v-if="features.baselayer" class="bottom-right-buttons">
          <div class="ui-button-wrapper">
            <button
              v-tippy="{ placement: 'left' }"
              class="iconbutton"
              :class="{ isActive: showBaseLayersPanel }"
              content="Basislagen"
              aria-label="Toon basislagen"
              :aria-expanded="showBaseLayersPanel.toString()"
              aria-controls="baseLayers"
              @click="toggleBaseLayersPanel"
            >
              <MapIcon />
            </button>
          </div>
          <transition name="fade">
            <BaseLayersPanel v-if="showBaseLayersPanel" :layers="baseLayers" @toggle-layer="toggleLayer" />
          </transition>
        </div>
        <div v-if="!isEmbed && (panoramaViewers.length > 0 || obliqueViewers.length > 0)" class="bottom-right-buttons">
          <div class="ui-button-wrapper">
            <button
              v-if="panoramaViewers.length > 0"
              v-tippy="{ placement: 'left' }"
              class="iconbutton __inverse"
              :class="{ isActive: showPanoramaPanel }"
              content="Rondkijkfoto"
              aria-label="Toon rondkijkfoto"
              @click="togglePanoramaPanel"
            >
              <PanoramaIcon class="icon" />
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
        <PrintModal
          v-if="modal === 'print'"
          :loading="loadingPrint"
          @toggle-modal="toggleModal"
          @print-map-to-pdf="printMapToPdf"
        />
        <DrawingModal v-if="modal === 'drawing'" :layers="layers" :position="position" @toggle-modal="toggleModal" />
      </div>
    </transition>
    <AlertMessage :alert="alert" />
  </div>
</template>

<script>
import ListIcon from "../../assets/icons/list-icon.svg";
import GeoJSON from "ol/format/GeoJSON";
import TileWMS from "ol/source/TileWMS";
import View from "ol/View";
import OpenLayersRenderer from "./renderers/OpenLayers/OpenLayers";
import { getFetchParameters } from "../../utils/auth";

import PrimaryButton from "../PrimaryButton";
import ListPanel from "../ListPanel";
import FilterPanel from "../FilterPanel";
import DataPanel from "../DataPanel";
import PointInfoPanel from "../PointInfoPanel";
import DetailPanel from "../DetailPanel";
import SearchPanel from "../SearchPanel";
import LayersPanel from "../LayersPanel";
import ToolsPanel from "../tools/ToolsPanel.vue";
import ZoomPanel from "../ZoomPanel";
import GeoLocationButton from "../GeoLocationButton";
import FilterListIcon from "../../assets/icons/filter-list-icon.svg";
import DataPanelButton from "../DataPanelButton.vue";
import { isMobile } from "@/utils/helpers";
import { transform } from "ol/proj";
import BaseLayersPanel from "@/components/BaseLayersPanel.vue";
import MapIcon from "../../assets/icons/map-icon.svg";
import PanoramaIcon from "../../assets/icons/panorama-icon.svg";
import ObliqueIcon from "../../assets/icons/oblique-icon.svg";
import MorePanel from "@/components/MorePanel.vue";
import nunjucks from "nunjucks";
import PrintModal from "@/components/PrintModal.vue";
import DrawingModal from "@/components/DrawingModal.vue";
import AlertMessage from "@/components/AlertMessage.vue";
import EmbedModal from "@/components/EmbedModal.vue";
import { useGlobalStore } from "@/stores";
import { mapStores } from "pinia";
import PanoramaPanel from "../PanoramaPanel.vue";
import { useMapStore } from "@/stores/map_store";
import {
  DEFAULT_DRAWING_COLOR,
  DEFAULT_DRAWING_FONT_SIZE,
  DEFAULT_DRAWING_STROKE_WIDTH,
} from "@/components/constants/defaults";

const reverseGeocodingEndpoint = "https://api.pdok.nl/bzk/locatieserver/search/v3_1/reverse";

export default {
  name: "MapRenderer",
  components: {
    PanoramaPanel,
    EmbedModal,
    AlertMessage,
    DrawingModal,
    PrintModal,
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
    mapId: String,
    initialLayers: Array,
    initialPosition: Object,
    initialDrawFeatures: Array,
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
    adminMap: {
      type: Boolean,
      default: () => {
        return false;
      },
    },
  },
  data() {
    return {
      layers: this.initialLayers,
      position: this.initialPosition,
      drawFeatures: [],
      removedDrawFeatures: [],
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
      infoPanelExpanded: false,
      mapStore: null,
      mapPadding: [0, 0, 0, 0],
      computedStyle: {},
      modal: "",
      interaction: "",
      userLayerSettings: {},
      undoRedoInteraction: null,
      color: DEFAULT_DRAWING_COLOR,
      strokeWidth: DEFAULT_DRAWING_STROKE_WIDTH,
      fontSize: DEFAULT_DRAWING_FONT_SIZE,
      showPanoramaPanelFullScreen: false,
      loadingPrint: false,
    };
  },
  computed: {
    ...mapStores(useGlobalStore),
    showInfoPanel() {
      return this.position.marker ? true : false;
    },
    panoramaViewers() {
      return this.config.viewers.filter((v) => !v.is_oblique);
    },
    obliqueViewers() {
      return this.config.viewers.filter((v) => v.is_oblique);
    },
    obliqueViewerUrl() {
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
    mapArea() {
      if (!this.config.map_area) {
        return;
      }

      const geojsonFormat = new GeoJSON();
      return geojsonFormat.readFeatures(this.config.map_area);
    },
    selectedAreaDataPanel() {
      if (this.tool === "SELECT_AREA" || this.tool === "SELECT_CIRCLE") {
        return this.selectedArea;
      }

      return null;
    },
    regularLayers() {
      return this.layers.filter((l) => !l.is_base);
    },
    baseLayers() {
      return this.layers.filter((l) => l.is_base);
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

        if (this.adminMap) {
          // Update the objects in user layer settings according to available layers.
          const newLayerIds = new Set(this.layers.map((layer) => layer.id));

          // Remove userLayerSettings entries that are not in the new layers
          Object.keys(this.userLayerSettings).forEach((layerId) => {
            if (!newLayerIds.has(layerId)) {
              delete this.userLayerSettings[layerId];
            }
          });

          // Add missing userLayerSettings entries for new layers
          this.layers.forEach((layer) => {
            if (!(layer.id in this.userLayerSettings)) {
              this.userLayerSettings[layer.id] = {};
            }
          });
        }
      },
      deep: true,
    },
    initialDrawFeatures: {
      handler(value) {
        this.drawFeatures = value;
      },
      deep: true,
      immediate: true,
    },
    userLayerSettings: {
      handler(value) {
        this.$emit("update-user-settings", value);
      },
      deep: true,
    },
  },
  mounted() {
    window.addEventListener("resize", this.onResizeWindow);
    this.setViewportHeight();

    this.mapStore = useMapStore(this.mapId);
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
          `${reverseGeocodingEndpoint}?X=${position.marker[0]}&Y=${position.marker[1]}&rows=1&distance=20`,
        );
        const data = await result.json();

        const coordinates = `${Math.round(position.marker[0] * 100) / 100}, ${
          Math.round(position.marker[1] * 100) / 100
        }`;

        const convertedPosition = transform([position.marker[0], position.marker[1]], "EPSG:28992", "EPSG:4326");
        const coordEPSG4326 = `${Math.round(convertedPosition[1] * 1000) / 1000}, ${
          Math.round(convertedPosition[0] * 1000) / 1000
        }`;

        if (!data.response.docs || data.response.docs.length === 0) {
          this.globalStore.setSearchQuery({ coordinates: coordinates, coordEPSG4326: coordEPSG4326 });
          return;
        }

        const object = data.response.docs[0];
        this.globalStore.setSearchQuery({
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
          const result = await fetch(url, getFetchParameters(layer, this.user));
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
    printMapToPdf(settings) {
      this.$refs.map.printToPdf(settings);
    },
    drawingSaved(id) {
      this.globalStore.setDrawing(id);
      this.modal = "drawing";
    },
    toggleModal(modal) {
      this.modal = modal;
    },
    togglePanoramaPanel() {
      this.showBaseLayersPanel = false;
      this.showPanoramaPanel = !this.showPanoramaPanel;

      if (!this.showPanoramaPanel) {
        this.showPanoramaPanelFullScreen = false;
      }
    },
    togglePanoramaPanelFullScreen(fullscreen) {
      this.showPanoramaPanelFullScreen = fullscreen;
    },
    toggleDataPanel() {
      this.showDataPanel = !this.showDataPanel;
      if (!this.showDataPanel) {
        // Reset selected area and make sure tool is no longer set to measure.
        this.selectedArea = null;
        this.setTool("");
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
        this.mapPadding[3] = 0;
        return;
      }

      if (this.showDataPanel && !this.showDataPanelFullScreen) {
        this.mapPadding[3] = window.innerWidth * 0.5;
        return;
      }

      if (this.showInfoPanel) {
        if (this.infoPanelExpanded) {
          this.mapPadding[3] = window.innerWidth * 0.5;
          return;
        }

        this.mapPadding[3] = window.innerWidth * 0.25;
        return;
      }

      // reset padding of the inner window.
      this.mapPadding[3] = 0;
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
          this.globalStore.setSelectedArea(result.sketch.getGeometry());
          break;
        case "SELECT_AREA":
        case "SELECT_CIRCLE":
          this.showDataPanel = true;
          this.selectedArea = result.sketch.getGeometry();
          this.globalStore.setSelectedArea(result.sketch.getGeometry());
          break;
        case "DRAW_POINT":
        case "DRAW_LINE":
        case "DRAW_POLYGON":
        case "DRAW_COORDINATE":
        case "DRAW_LABEL":
          this.drawFeatures.push(result.sketch);
          this.removedDrawFeatures = [];
          break;
        case "EDIT_POINT":
        case "EDIT_LINE":
        case "EDIT_POLYGON":
          console.log("damn");
          break;
      }
    },
    setInteraction(interaction) {
      if (interaction === "UNDO" && this.drawFeatures.length) {
        this.removedDrawFeatures.push(this.drawFeatures.pop());
      }

      if (interaction === "REDO" && this.removedDrawFeatures.length) {
        this.drawFeatures.push(this.removedDrawFeatures.pop());
      }
    },
    featuresSelected(selectedFeatures) {
      this.selectedFeatures = selectedFeatures;
    },
    setSelectedArea(selectedArea) {
      this.selectedArea = selectedArea;
    },
    toggleLayer([layerId, isVisible]) {
      this.layers = this.layers.map((layer) => (layer.id === layerId ? { ...layer, is_visible: isVisible } : layer));
      this.userLayerSettings[layerId] = { ...this.userLayerSettings[layerId], is_visible: isVisible };
      this.$emit("layers-changed", this.layers);
      this.mapStore.resetFiltersForLayer(layerId);
    },
    setLayerOpacity([layerId, opacity]) {
      this.layers = this.layers.map((layer) => (layer.id === layerId ? { ...layer, opacity: opacity } : layer));
      this.userLayerSettings[layerId] = { ...this.userLayerSettings[layerId], opacity: opacity };
      this.$emit("layers-changed", this.layers);
    },
    onToggleIsSelectable([layerId, isSelectable]) {
      this.layers = this.layers.map((layer) =>
        layer.id === layerId ? { ...layer, is_selectable: isSelectable } : layer,
      );
      this.setPosition(this.position);
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
    onFit(position, halfScreen) {
      // Since onFit is called before the data panel is open we need to make sure the
      // mapPadding is set correctly.
      if (halfScreen && !isMobile()) {
        this.mapPadding[3] = window.innerWidth * 0.5;
      }
      this.$refs.map.fit(position, { maxZoom: 19 });
    },
    setColor(color) {
      this.color = color;
    },
    setStrokeWidth(strokeWidth) {
      this.strokeWidth = strokeWidth;
    },
    setFontSize(fontSize) {
      this.fontSize = fontSize;
    },
    setLoadingPrint(loading) {
      this.loadingPrint = loading;
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

/* When portal header is active its height must be subtracted of total height. */
.map-container.portalHeader {
  height: calc(100dvh - 55px);
}

.renderer-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-flow: column;
  background: var(--color-white);
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

.ui-button-wrapper {
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: var(--radius-normal);
  overflow: hidden;
  box-shadow: var(--shadow-normal);
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

.toggle-buttons.position-top {
  top: 0;
}

@media (max-width: 576px) {
  .toggle-buttons {
    top: calc(var(--padding-screen) * 2 + var(--width-button-large));
    left: var(--padding-screen);
  }

  .toggle-buttons.position-top {
    top: var(--padding-screen);
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
  transition:
    width 0.1s ease,
    border-radius 0.1s;
  height: var(--width-button-large);
}

.bottom-right-buttons {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  background: white;
  border-radius: var(--radius-normal);
  box-shadow: var(--shadow-normal);
  transition:
    height 0.1s ease,
    border-radius 0.1s;
}

.bottom-right-buttons .iconbutton {
  width: var(--width-button-normal);
  height: var(--width-button-normal);
}

.bottom-right-buttons .iconbutton:first-child & .iconbutton:not(:only-child) {
  box-sizing: content-box;
  border-bottom: 1px solid var(--color-grey-50);
}

.panorama-splitter {
  z-index: 2;
}
</style>
