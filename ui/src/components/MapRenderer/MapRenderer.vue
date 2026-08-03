<template>
  <Toast position="bottom-center" />
  <div
    id="map-container"
    ref="mapContainer"
    class="map-container"
    :class="{ showInfoPanel, showDataPanel, portalHeader: !isEmbed && config.features.portal }"
    :style="computedStyle"
  >
    <div class="renderer-container">
      <ConfirmPopup group="templating">
        <template #message="slotProps">
          <div class="tw-px-4">
            <i :class="slotProps.message.icon" class=""></i>
            <p>{{ slotProps.message.message }}</p>
          </div>
        </template>
      </ConfirmPopup>
      <Splitter
        v-if="!isEmbed && (panoramaViewers.length > 0 || obliqueViewers.length > 0)"
        ref="splitter"
        style="height: 100vh"
        layout="vertical"
        @resizeend="onSplitterResizeEnd"
      >
        <SplitterPanel v-if="showPanoramaPanel" class="flex items-center justify-center panorama-splitter">
          <PanoramaPanel
            class="panorama-panel"
            :map-id="mapId"
            :position="position"
            @toggle="togglePanoramaPanel"
            @toggle-full-screen="togglePanoramaPanelFullScreen"
            @position-changed="setPosition"
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
            :measured-areas="measuredAreas"
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
            :show-compare-slider="compareLayers"
            @position-changed="setPosition"
            @tool-used="toolUsed"
            @features-selected="featuresSelected"
            @on-fit="(position) => onFit(position)"
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
        :measured-areas="measuredAreas"
        :highlighted-features="highlightedFeatures"
        :selected-features="selectedFeatures"
        :show-compare-slider="compareLayers"
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
        @on-fit="(position) => onFit(position)"
        @loading-print-to-pdf="setLoadingPrint"
      />
    </div>
    <AboutPanel
      v-if="!isEmbed && !showPanoramaPanel && showAbout"
      :features="features"
      :about="about"
      :about-title="aboutTitle"
      :thumbnail="thumbnail"
      :show-panel="showAbout"
      @close-side-panel="closeAbout"
      @hide-panel="closeAbout"
      @toggle-modal="toggleModal"
      @toggle-about="toggleAbout"
    />
    <ListPanel
      v-if="showList && layers.length > 0"
      ref="listPanel"
      :map-id="mapId"
      :layer="getSelectedLayer(settings.listLayerId)"
      :title-template="settings.title"
      :short-description-template="settings.short_description"
      @hide-panel="toggleList"
      @show-feature-on-map="showFeatureOnMap"
    />
    <FilterPanel
      v-if="showFilters"
      ref="filterPanel"
      :layer="getSelectedLayer(settings.filterLayerId)"
      :facets="settings.facets"
      :user="user"
      :map-id="mapId"
      @hide-panel="toggleFilters"
    />
    <PointInfoPanel
      v-if="!showPanoramaPanel && features.markerOnClick"
      :layers="layers"
      :position="position"
      :show-panel="!showDataPanel && showInfoPanel && !editLayerStore.hideOtherPanels"
      :user="user"
      :config="config"
      :features="features"
      :map-id="mapId"
      @set-position="setPosition"
      @on-fit="onFit"
      @expanded-info-panel="toggleInfoPanel"
      @select-feature="selectFeature"
      @show-feature-on-map="showFeatureOnMap"
    />
    <DetailPanel
      v-if="!showPanoramaPanel && !features.markerOnClick && features.detail"
      :show-panel="selectedFeatures.length > 0 && !editLayerStore.hideOtherPanels"
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
      @show-feature-on-map="showFeatureOnMap"
      @toggle-data-panel="toggleDataPanel"
      @toggle-full-side-panel="toggleDataPanelFullScreen"
    />
    <AddFeaturePanel
      :user="user"
      :refresh-layer="refreshLayer"
      @set-tool="setTool"
      @set-selected-area="setSelectedArea"
    />
    <EditFeaturePanel :user="user" :refresh-layer="refreshLayer" @set-tool="setTool" />

    <CompareLayersPanel
      :map-id="mapId"
      :show-compare-layer-panel="showCompareLayerPanel"
      :layers="wmsWfsAndWMTSLayers"
      @close-panel="closeCompareLayerPanel"
      @stop-compare="stopCompareLayers"
    />
    <TimeSliderPanel
      :map-id="mapId"
      :show-time-slider-panel="mapStore.showTimeSliderPanel"
      :layers="layers"
      @close-panel="closeTimeSliderPanel"
      @disable-time-slider="disableTimeSlider"
    />

    <div v-show="!showDataPanel || !showDataPanelFullScreen" class="ui-container">
      <div class="top-left-panels" :class="{ 'extra-padding': showInfoPanel || showDataPanel }">
        <div class="toggle-buttons" :class="{ 'position-top': !features.searchbar }">
          <div v-if="features.datapanel && !features.searchbar" class="datapanel-btn-wrapper">
            <DataPanelButton :show-data-panel="showDataPanel" :map-id="mapId" @show-data-panel="toggleDataPanel" />
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
            :badge="countOfActiveSelectedFiltersForLayer"
            @on-button-click="toggleFilters"
          >
            <FilterListIcon />
          </PrimaryButton>
          <PrimaryButton
            v-if="
              features.resetButton &&
              !isEmbed &&
              !hideResetButton &&
              (countOfLayersWithActiveFilters > 0 ||
                mapStore?.visibleLayers?.length > 0 ||
                baseLayerChanged ||
                newDrawing ||
                selectedArea)
            "
            v-tooltip="'Wis alle filters, lagen, getekende objecten, geselecteerde gebieden en instellingen'"
            size="large"
            label="Herstel"
            drop-shadow
            @on-button-click="confirmResetMap($event)"
          >
            <i class="pi pi-refresh"></i>
          </PrimaryButton>
        </div>
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
          :map-ref="$refs.map"
          :map-id="mapId"
          @set-tool="setTool"
          @set-selected-area="setSelectedArea"
          @drawing-saved="drawingSaved"
          @clear-draw="clearDrawing"
          @set-interaction="setInteraction"
          @set-color="setColor"
          @set-stroke-width="setStrokeWidth"
          @set-font-size="setFontSize"
        />
        <MorePanel
          v-if="features.morepanel && !isEmbed && !showPanoramaPanel"
          :user="user"
          :show-disclaimer="config.show_disclaimer"
          @toggle-modal="toggleModal"
          @toggle-about="toggleAbout"
        />
      </div>
      <div class="bottom-left-panels" :class="{ 'bottom-panels-padding': compareLayers || mapStore.timeSlider }">
        <LayersPanel
          v-if="features.layerlist || features.legend"
          :layers="regularLayers"
          :layer-tree="layerTree"
          :position="position"
          :user="user"
          :map-id="mapId"
          :show-search-bar="features.layerlistsearch"
          :show-simple-layer-list="features.layerlistsimple"
          :show-compare-slider="compareLayers"
          :layer-panel-collapsed="features.layerPanelCollapsed"
          :is-embed="features.legend && !features.layerlist"
          @on-fit="(layer) => $refs.map.fit(layer)"
          @set-position="setPosition"
        />
      </div>
      <div class="bottom-center-panels">
        <CompareLayersSlider :map-id="mapId" :show-compare-layer-panel="compareLayers" />
        <TimeSliderSlider :map-id="mapId" :show-time-slider="mapStore.timeSlider" />
      </div>
      <div class="bottom-right-panels" :class="{ 'bottom-panels-padding': compareLayers || mapStore.timeSlider }">
        <div v-if="features.baselayer" class="bottom-right-buttons">
          <div class="ui-button-wrapper">
            <button
              v-tippy="{ placement: 'left' }"
              class="iconbutton"
              :class="{ isActive: showBaseLayersPanel }"
              content="Basislagen"
              aria-label="Toon basislagen"
              data-testid="toggle-base-layers"
              :aria-expanded="showBaseLayersPanel.toString()"
              aria-controls="baseLayers"
              @click="toggleBaseLayersPanel"
            >
              <MapIcon />
            </button>
          </div>
          <transition name="fade">
            <BaseLayersPanel v-if="showBaseLayersPanel" :map-id="mapId" />
          </transition>
        </div>
        <div v-if="mapStore.visibleLayersForTimeSliderPanel.length > 0" class="bottom-right-buttons">
          <div class="ui-button-wrapper">
            <button
              v-tippy="{ placement: 'left' }"
              class="iconbutton __inverse"
              :class="{ isActive: mapStore.timeSlider }"
              content="Tijdlijn bekijken"
              aria-label="Tijdlijn bekijken"
              @click="toggleTimeSliderPanel"
            >
              <i class="pi pi-history"></i>
            </button>
          </div>
        </div>
        <div v-if="features.compareLayers" class="bottom-right-buttons">
          <div class="ui-button-wrapper">
            <button
              v-tippy="{ placement: 'left' }"
              class="iconbutton __inverse"
              :class="{ isActive: compareLayers }"
              content="Vergelijk kaartlagen"
              aria-label="Vergelijk kaartlagen"
              @click="toggleCompareLayerPanel"
            >
              <CompareLayersIcon />
            </button>
          </div>
        </div>
        <div
          v-if="features.panoramaViewers && !isEmbed && (panoramaViewers.length > 0 || obliqueViewers.length > 0)"
          class="bottom-right-buttons"
        >
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
      <div v-if="modal === 'embed' || modal === 'print' || modal === 'drawing'">
        <EmbedModal
          v-if="modal === 'embed'"
          :map-id="mapId"
          :layers="layers"
          :position="position"
          @toggle-modal="toggleModal"
        />
        <PrintModal
          v-if="modal === 'print'"
          :loading="loadingPrint"
          @toggle-modal="toggleModal"
          @print-map-to-pdf="printMapToPdf"
        />
        <DrawingModal
          v-if="modal === 'drawing'"
          :layers="layers"
          :position="position"
          :map-id="mapId"
          :drawing-id="drawingId"
          @toggle-modal="toggleModal"
        />
      </div>
    </transition>
    <AlertMessage :alert="alert" />
  </div>
</template>

<script>
import AlertMessage from "@/components/AlertMessage.vue";
import BaseLayersPanel from "@/components/BaseLayersPanel.vue";
import DrawingModal from "@/components/DrawingModal.vue";
import EmbedModal from "@/components/EmbedModal.vue";
import MorePanel from "@/components/MorePanel.vue";
import PrintModal from "@/components/PrintModal.vue";
import { useGlobalStore } from "@/stores";
import { useMapStore } from "@/stores/map_store";
import { isMobile } from "@/utils/helpers";
import nunjucks from "nunjucks";
import GeoJSON from "ol/format/GeoJSON";
import { transform } from "ol/proj";
import TileWMS from "ol/source/TileWMS";
import View from "ol/View";
import { mapStores } from "pinia";
import { useConfirm } from "primevue";
import FilterListIcon from "../../assets/icons/filter-list-icon.svg";
import ListIcon from "../../assets/icons/list-icon.svg";
import MapIcon from "../../assets/icons/map-icon.svg";
import ObliqueIcon from "../../assets/icons/oblique-icon.svg";
import PanoramaIcon from "../../assets/icons/panorama-icon.svg";
import CompareLayersIcon from "../../assets/icons/compare-layers-icon.svg";
import { getFetchParameters } from "../../utils/auth";
import AboutPanel from "../AboutPanel";
import DataPanel from "../DataPanel";
import DataPanelButton from "../DataPanelButton.vue";
import DetailPanel from "../DetailPanel";
import FilterPanel from "../FilterPanel";
import GeoLocationButton from "../GeoLocationButton";
import LayersPanel from "../LayersPanel";
import ListPanel from "../ListPanel";
import PanoramaPanel from "../PanoramaPanel.vue";
import PointInfoPanel from "../PointInfoPanel";
import PrimaryButton from "../PrimaryButton";
import SearchPanel from "../SearchPanel";
import ToolsPanel from "../tools/ToolsPanel.vue";
import ZoomPanel from "../ZoomPanel";
import OpenLayersRenderer from "./renderers/OpenLayers/OpenLayers";
import CompareLayersPanel from "@/components/compare-layers/CompareLayersPanel.vue";
import CompareLayersSlider from "@/components/compare-layers/CompareLayersSlider.vue";
import TimeSliderPanel from "@/components/time-slider/TimeSliderPanel.vue";
import TimeSliderSlider from "@/components/time-slider/TimeSliderSlider.vue";
import { DEFAULT_DRAWING_COLOR, DEFAULT_DRAWING_FONT_SIZE, DEFAULT_DRAWING_STROKE_WIDTH } from "@/constants/defaults";
import { useEditLayerStore } from "@/stores/edit_layer_store";
import AddFeaturePanel from "@/components/edit-layers/AddFeaturePanel.vue";
import EditFeaturePanel from "@/components/edit-layers/EditFeaturePanel.vue";
import { createMeasurementTooltip } from "@/utils/measure-tooltip";
import { getFeatureCenterCoordinates } from "@/utils/geometry-helpers";
import { pushHistoryState } from "@/utils/map-url-utils";
import { ELayerTypes } from "@/types/layer";
import { finalizeMultipartFeatureOnEnter, handleEditLayerToolUsed } from "@/components/MapRenderer/utils/edit-layer";
import { getWmsTimeParameter } from "@/utils/wms-time";

const reverseGeocodingEndpoint = "https://api.pdok.nl/bzk/locatieserver/search/v3_1/reverse";
const MAP_PADDING_RIGHT_INDEX = 3;
const DEFAULT_PANEL_WIDTH = 280;

export default {
  name: "MapRenderer",
  components: {
    TimeSliderSlider,
    TimeSliderPanel,
    CompareLayersSlider,
    CompareLayersPanel,
    EditFeaturePanel,
    AddFeaturePanel,
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
    AboutPanel,
    DetailPanel,
    ListPanel,
    FilterPanel,
    OpenLayersRenderer,
    ToolsPanel,
    ZoomPanel,
    GeoLocationButton,
    DataPanelButton,
    MapIcon,
    CompareLayersIcon,
    PanoramaIcon,
    ObliqueIcon,
  },
  props: {
    mapId: String,
    about: {
      type: String,
      required: false,
      default: "",
    },
    aboutTitle: {
      type: String,
      required: false,
      default: "",
    },
    thumbnail: {
      type: String,
      required: false,
      default: "",
    },
    initialLayers: Array,
    layerTree: {
      type: Array,
      default: () => [],
    },
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
    adminMap: {
      type: Boolean,
      default: () => {
        return false;
      },
    },
    hideResetButton: {
      type: Boolean,
      default: () => {
        return false;
      },
    },
  },
  data() {
    return {
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
      showAbout: false,
      showList: false,
      showFilters: false,
      infoPanelExpanded: false,
      mapStore: null,
      mapPadding: [0, 0, 0, 0],
      computedStyle: {},
      modal: "",
      interaction: "",
      undoRedoInteraction: null,
      color: DEFAULT_DRAWING_COLOR,
      strokeWidth: DEFAULT_DRAWING_STROKE_WIDTH,
      fontSize: DEFAULT_DRAWING_FONT_SIZE,
      showPanoramaPanelFullScreen: false,
      loadingPrint: false,
      showCompareLayerPanel: false,
      compareLayers: false,
      selectGeometry: false,
      filterCheckedCount: 0,
      baseLayerChanged: false,
      initialBaseLayerId: null,
      initialDrawing: null,
      confirm: useConfirm(),
      newDrawing:
        JSON.stringify(this.initialDrawing) !== JSON.stringify(this.drawFeatures) ||
        (!this.initialDrawing && this.drawFeatures?.length > 0),
      showNotAllowedToEditLayerModal: false,
      editLayerName: null,
    };
  },
  computed: {
    ...mapStores(useGlobalStore, useEditLayerStore, useMapStore),
    layers() {
      return this.mapStore ? this.mapStore.layers : [];
    },
    measuredAreas() {
      return this.mapStore.measuredAreas;
    },
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
      if (this.tool === "SELECT_AREA" || this.tool === "SELECT_CIRCLE" || this.selectGeometry) {
        return this.selectedArea;
      }

      return null;
    },
    regularLayers() {
      return this.mapStore ? this.mapStore.regularLayers : [];
    },
    wmsWfsAndWMTSLayers() {
      return this.mapStore ? this.mapStore.wmsWfsAndWMTSLayers : [];
    },
    countOfLayersWithActiveFilters() {
      return this.mapStore ? this.mapStore.getActiveLayersWithFilterCount : 0;
    },
    countOfActiveSelectedFiltersForLayer() {
      return this.mapStore && this.settings.facets
        ? this.mapStore.getActiveSelectedItemCountPerFilterForLayer(this.settings.filterLayerId, this.settings.facets)
        : 0;
    },
    drawingId() {
      return this.mapStore ? this.mapStore.drawingId : null;
    },
  },
  watch: {
    initialPosition: {
      handler(value) {
        this.position = value;
      },
      deep: true,
    },
    "mapStore.layers": {
      handler(value) {
        if (!this.adminMap) {
          pushHistoryState(
            this.position,
            this.mapStore.selectedBaseLayer,
            this.mapStore.visibleLayers,
            this.drawingId,
            this.isEmbed,
          );
        }

        // Notify parent window if in embed mode
        if (this.isEmbed && window.parent !== window) {
          this.notifyIframeParentOfStateChange();
        }

        const editableLayers = value.filter(
          (layer) =>
            layer.is_visible && layer.can_write && (layer.source_type === "WMS_WFS" || layer.source_type === "WFS"),
        );

        this.editLayerStore.setEditableLayers(editableLayers);
      },
      deep: true,
    },
    // Don't highlight features on the map after editing
    "editLayerStore.modifiedFeature": {
      handler(value) {
        if (value) {
          this.highlightedFeatures = [];
        }
      },
      deep: true,
    },
    initialLayers: {
      handler(value) {
        const layersCopy = value.map((layer) => ({ ...layer }));

        this.mapStore.setLayers(layersCopy);
        this.mapStore.setBaseLayer(layersCopy.find((l) => l.is_base && l.is_visible));
        this.mapStore.activateVisibleTimeSliderLayer();
      },
      deep: true,
    },
    features: {
      handler(value) {
        this.showAbout = value.showAbout ? value.showAbout : false;
      },
      deep: true,
    },
  },
  created() {
    this.mapStore = useMapStore(this.mapId);

    const layersCopy = this.initialLayers.map((layer) => ({ ...layer }));

    // Store initial base layer ID
    const initialBaseLayer = layersCopy.find((l) => l.is_base && l.is_visible);
    if (initialBaseLayer) {
      this.initialBaseLayerId = initialBaseLayer.id;
    }

    this.mapStore.setLayers(layersCopy);
    this.mapStore.setBaseLayer(initialBaseLayer);
    this.mapStore.activateVisibleTimeSliderLayer();

    if (this.globalStore.drawing) {
      this.mapStore.setDrawingId(this.globalStore.drawing);
      this.fetchDrawing();
    }
  },
  mounted() {
    window.addEventListener("resize", this.onResizeWindow);
    document.addEventListener("keydown", this.finalizeMultipartFeatureOnEnter);
    this.$nextTick(() => {
      this.setViewportHeight();
    });
    this.showAbout = this.features.showAbout ? this.features.showAbout : false;
  },
  unmounted() {
    window.removeEventListener("resize", this.onResizeWindow);
    document.removeEventListener("keydown", this.finalizeMultipartFeatureOnEnter);
  },
  methods: {
    finalizeMultipartFeatureOnEnter(event) {
      if (event.key !== "Enter") {
        return;
      }

      finalizeMultipartFeatureOnEnter({
        editLayerStore: this.editLayerStore,
        tool: this.tool,
        clearTool: () => this.setTool(""),
      });

      event.preventDefault();
    },
    notifyIframeParentOfStateChange() {
      // Notifies the parent window of active layer, zoom, and position changes
      // while configuring the embed, so it can update the embed URL accordingly.
      if (!window.parent || window.parent === window) {
        return;
      }

      const serializablePosition = {
        center: this.position.center ? [this.position.center[0], this.position.center[1]] : null,
        zoom: this.position.zoom,
      };

      const serializableLayers = this.mapStore.layers.map((layer) => ({
        id: layer.id,
        is_visible: layer.is_visible,
        is_base: layer.is_base,
        name: layer.name,
      }));

      window.parent.postMessage(
        {
          type: "map-state-update",
          position: serializablePosition,
          layers: serializableLayers,
        },
        window.location.origin,
      );
    },
    onResizeWindow() {
      this.setViewportHeight();
    },
    onSplitterResizeEnd() {
      this.$nextTick(() => {
        this.setViewportHeight();
      });
    },
    setViewportHeight() {
      const mapViewportHeight = this.$refs.map?.$el?.clientHeight;
      const fallbackContainerHeight = this.$refs.mapContainer?.clientHeight ?? window.innerHeight;
      const resolvedHeight = Number.isFinite(mapViewportHeight) ? mapViewportHeight : fallbackContainerHeight;
      this.computedStyle["--vh"] = `${resolvedHeight / 100}px`;
    },
    async setPosition(position, animateFast = false, animate = true) {
      this.position = {
        ...position,
        animateFast: animateFast,
        animate: animate,
      };

      if (!this.adminMap) {
        pushHistoryState(
          this.position,
          this.mapStore.selectedBaseLayer,
          this.mapStore.visibleLayers,
          this.drawingId,
          this.isEmbed,
        );
      }

      // Notify parent window if in embed mode
      if (this.isEmbed && window.parent !== window) {
        this.notifyIframeParentOfStateChange();
      }

      if (!position.marker) {
        this.highlightedFeatures = [];
        return;
      }

      this.setWindowInnerWidth();

      this.reverseGeocode(position);

      // Skip `getFeatureInfo` when the position change came from the map itself (`ol-view`)
      // or from `showFeatureOnMap` (`show-feature`). Those flows update the view or display
      // an already known feature, so they should not trigger a new feature-info lookup.
      if (position.source !== "ol-view" && position.source !== "show-feature") {
        this.getFeatureInfo(position);
      }
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

      this.mapStore.visibleLayersForFeatures.forEach(async (layer) => {
        if (layer.source_type === ELayerTypes.WMTS) {
          return;
        }

        const timeParameter = getWmsTimeParameter(this.mapStore, layer.id, layer.is_time_enabled === true);

        const wmsSource = new TileWMS({
          url: layer.url,
          servertype: layer.server_type,
          params: {
            LAYERS: layer.name,
            ...(timeParameter ? { TIME: timeParameter } : {}),
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
          const features = data.features.map((feature) => new GeoJSON().readFeature(feature));
          this.highlightedFeatures = [...this.highlightedFeatures, ...features];

          if (this.$refs.map && this.$refs.map.map) {
            const tooltip = createMeasurementTooltip(features[0], this.$refs.map.map, { isStatic: true });
            if (tooltip) {
              this.$refs.map.measuredAreaTooltips.push(tooltip);
            }
          }
        } catch (e) {
          console.error(e);
        }
      });
    },
    printMapToPdf(settings) {
      this.$refs.map.printToPdf(settings);
    },
    async fetchDrawing() {
      const response = await fetch(`/atlas/api/v1/drawings/${this.drawingId}/`);
      if (!response.ok) {
        return false;
      }

      const data = await response.json();

      const geojsonFormat = new GeoJSON();
      this.drawFeatures = data.features.map((feature) => geojsonFormat.readFeature(feature));
    },
    drawingSaved(id) {
      if (!this.adminMap) {
        pushHistoryState(this.position, this.mapStore.selectedBaseLayer, this.mapStore.visibleLayers, id, this.isEmbed);
      }

      this.mapStore.setDrawingId(id);
      this.modal = "drawing";
    },
    clearDrawing() {
      this.drawFeatures = [];
      this.mapStore.setDrawingId(null);
      if (!this.adminMap) {
        pushHistoryState(
          this.position,
          this.mapStore.selectedBaseLayer,
          this.mapStore.visibleLayers,
          null,
          this.isEmbed,
        );
      }
    },
    toggleModal(modal) {
      this.modal = modal;
    },
    toggleShowNotAllowedtoEditLayerModal() {
      this.showNotAllowedToEditLayerModal = false;
      this.editLayerName = null;
    },
    togglePanoramaPanel() {
      this.showBaseLayersPanel = false;
      this.showPanoramaPanel = !this.showPanoramaPanel;

      if (!this.showPanoramaPanel) {
        this.showPanoramaPanelFullScreen = false;
      }

      this.$nextTick(() => {
        this.setViewportHeight();
      });
    },
    togglePanoramaPanelFullScreen(fullscreen) {
      this.showPanoramaPanelFullScreen = fullscreen;

      this.$nextTick(() => {
        this.setViewportHeight();
      });
    },
    toggleDataPanel() {
      this.showDataPanel = !this.showDataPanel;
      if (!this.showDataPanel) {
        // Reset selected area and make sure tool is no longer set to measure.
        this.selectedArea = null;
        this.selectGeometry = false;
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
    closeAbout() {
      this.showAbout = false;
      this.setWindowInnerWidth();
    },
    setWindowInnerWidth() {
      // Do not adjust the inner window padding for mobile screens.
      if (isMobile()) {
        this.mapPadding[MAP_PADDING_RIGHT_INDEX] = 0;
        return;
      }

      if (this.showDataPanel && !this.showDataPanelFullScreen) {
        this.mapPadding[MAP_PADDING_RIGHT_INDEX] = window.innerWidth * 0.5;

        if (this.showList) {
          const listWidth = this.$refs.listPanel.$el.getBoundingClientRect().width ?? DEFAULT_PANEL_WIDTH;
          this.mapPadding[MAP_PADDING_RIGHT_INDEX] = this.mapPadding[3] + listWidth;
        }

        if (this.showFilters) {
          const filterWidth = this.$refs.filterPanel.$el.getBoundingClientRect().width ?? DEFAULT_PANEL_WIDTH;
          this.mapPadding[MAP_PADDING_RIGHT_INDEX] = this.mapPadding[MAP_PADDING_RIGHT_INDEX] + filterWidth;
        }

        return;
      }

      if (this.showInfoPanel) {
        if (this.infoPanelExpanded) {
          this.mapPadding[MAP_PADDING_RIGHT_INDEX] = window.innerWidth * 0.5;
          return;
        }

        this.mapPadding[MAP_PADDING_RIGHT_INDEX] = window.innerWidth * 0.25;
        return;
      }

      // reset padding of the inner window.
      this.mapPadding[MAP_PADDING_RIGHT_INDEX] = 0;
    },
    toggleList() {
      this.showList = !this.showList;
    },
    toggleFilters() {
      this.showFilters = !this.showFilters;
    },
    toggleAbout() {
      this.showAbout = !this.showAbout;
    },
    setTool(tool) {
      this.tool = tool;
    },
    toolUsed(result) {
      if (result && result.sketch && (result.tool === "SELECT_AREA" || result.tool === "SELECT_CIRCLE")) {
        this.selectedArea = result.sketch.getGeometry();
      }

      switch (result.tool) {
        case "MEASURE_AREA":
        case "MEASURE_LINE":
          this.mapStore.addMeasuredArea(result.sketch.getGeometry());
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
        case "Point":
        case "Polygon":
        case "LineString":
        case "LinearRing":
        case "Circle":
        case "MultiPoint":
        case "MultiLineString":
        case "MultiPolygon":
          handleEditLayerToolUsed({
            editLayerStore: this.editLayerStore,
            result,
            clearTool: () => this.setTool(""),
          });
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
    onFit(position) {
      this.$refs.map.fit(position, { maxZoom: 19, duration: 1000 });
    },
    async showFeatureOnMap(feature) {
      const geoFeature = new GeoJSON().readFeature(feature);
      const center = getFeatureCenterCoordinates(feature);

      await this.setPosition(
        {
          ...this.position,
          center,
          marker: center,
          zoom: 19,
          source: "show-feature",
        },
        false,
        false,
      );

      this.selectedFeatures = [];
      this.highlightedFeatures = [geoFeature];
      this.onFit(geoFeature.getGeometry());
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
    resetMap() {
      this.mapStore.resetAllFilters();

      // Check for /atlas/maps/ID pattern
      const mapsMatch = window.location.pathname.match(/\/atlas\/maps\/([^/]+)/);
      // Check for /atlas/@ pattern (direct coordinates)
      const coordsMatch = window.location.pathname.match(/\/atlas\/@([^/]+)/);
      // Check for drawing= in url
      const drawingMatch = window.location.pathname.match(/\/drawing=([^/]+)(?:\/|$)/);

      if (mapsMatch) {
        // Navigate to the new URL with just the position
        window.location.href = `${window.location.origin}/atlas/maps/${mapsMatch[1]}/${drawingMatch ? `drawing=${drawingMatch[1]}` : ""}`;
      } else if (coordsMatch) {
        // Navigate to the new URL with just the coordinates
        window.location.href = `${window.location.origin}/atlas/@${coordsMatch[1]}/${drawingMatch ? `drawing=${drawingMatch[1]}` : ""}`;
      } else {
        window.location.href = `${window.location.origin}/atlas/`;
      }
    },
    confirmResetMap(event) {
      if (!event) {
        return;
      }

      this.confirm.require({
        target: event.target,
        group: "templating",
        message: `Weet u zeker dat u alles wilt herstellen naar de standaard instellingen? Alle filters, lagen, getekende objecten, geselecteerde gebieden en instellingen worden verwijderd.`,
        rejectProps: {
          icon: "pi pi-times",
          label: "Annuleer",
          outlined: true,
        },
        acceptProps: {
          icon: "pi pi-refresh",
          label: "Herstel",
        },
        accept: () => {
          this.resetMap();
        },
        reject: () => {},
      });
    },
    toggleCompareLayerPanel() {
      if (!this.compareLayers) {
        this.compareLayers = true;
      }

      this.showCompareLayerPanel = !this.showCompareLayerPanel;
    },
    toggleTimeSliderPanel() {
      this.mapStore.toggleTimeSliderPanel();
    },
    closeCompareLayerPanel() {
      this.showCompareLayerPanel = false;
    },
    closeTimeSliderPanel() {
      this.mapStore.closeTimeSliderPanel();
    },
    disableTimeSlider() {
      this.mapStore.disableTimeSlider();
    },
    stopCompareLayers() {
      this.showCompareLayerPanel = false;
      this.compareLayers = false;
    },
    refreshLayer(id) {
      this.$refs.map.refreshLayer(id);
    },
    selectFeature(geometry) {
      this.selectedArea = geometry;
      this.selectGeometry = true;
      this.showDataPanel = true;
      this.$refs.map.fit(geometry, { maxZoom: 19, duration: 1000 });
      this.tool = "SELECT_FEATURE";
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

@media (max-width: 1024px) {
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

.bottom-center-panels {
  z-index: 1;
  position: absolute;
  bottom: var(--padding-screen);
  left: 0;
  right: 0;
  margin-inline: auto;
  width: fit-content;
  display: flex;
  flex-direction: column;
  gap: 12px;
  align-items: center;
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

@media (max-width: 640px) {
  .bottom-center-panels {
    width: 100%;
    padding: 0 var(--padding-screen);
  }

  .bottom-panels-padding {
    padding-bottom: 60px;
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
    width: 60vw;
    flex-wrap: wrap;
    top: calc(var(--padding-screen) * 2 + var(--width-button-large));
    left: var(--padding-screen);
  }

  .toggle-buttons.position-top {
    top: var(--padding-screen);
  }
}

.toggle-buttons > *:not(:last-child) {
  margin-right: 8px;
  margin-bottom: 8px;
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
