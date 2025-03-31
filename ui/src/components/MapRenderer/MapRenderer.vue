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
            :show-compare-slider="compareLayers"
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
        @on-fit="(position) => onFit(position, true)"
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
      @hidePanel="closeAbout"
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
      :show-panel="!showDataPanel && showInfoPanel && editLayerStore.editLayerMode === EditLayerMode.NONE"
      :user="user"
      :config="config"
      :features="features"
      @set-position="setPosition"
      @on-fit="(feature) => $refs.map.fit(feature, { maxZoom: 19, duration: 1000 })"
      @expanded-info-panel="toggleInfoPanel"
      @select-feature="selectFeature"
    />
    <DetailPanel
      v-if="!showPanoramaPanel && !features.markerOnClick && features.detail"
      :show-panel="selectedFeatures.length > 0 && editLayerStore.editLayerMode === EditLayerMode.NONE"
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
    <AddFeaturePanel
      :layers="regularLayers"
      :user="user"
      :refresh-layer="refreshLayer"
      @set-tool="setTool"
      @set-selected-area="setSelectedArea"
    />
    <EditFeaturePanel :user="user" :refresh-layer="refreshLayer" />

    <CompareLayersPanel
      :map-id="mapId"
      :show-compare-layer-panel="showCompareLayerPanel"
      :layers="wmsWfsLayers"
      @close-panel="closeCompareLayerPanel"
      @stop-compare="stopCompareLayers"
      @toggle-layer="toggleLayer"
    />

    <div v-show="!showDataPanel || !showDataPanelFullScreen" class="ui-container">
      <div class="top-left-panels" :class="{ 'extra-padding': showInfoPanel || showDataPanel }">
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
            :badge="countOfActiveSelectedFiltersForLayer"
            @on-button-click="toggleFilters"
          >
            <FilterListIcon />
          </PrimaryButton>
          <PrimaryButton
            v-if="
              !hideResetButton &&
              (countOfLayersWithActiveFilters > 0 ||
                visibleLayers.length > 0 ||
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
          @toggle-about="toggleAbout"
        />
      </div>
      <div class="bottom-left-panels" :class="{ 'bottom-panels-padding': compareLayers }">
        <LayersPanel
          v-if="features.layerlist || features.legend"
          :layers="regularLayers"
          :position="position"
          :user="user"
          :map-id="mapId"
          :show-search-bar="features.layerlistsearch"
          :show-simple-layer-list="features.layerlistsimple"
          :show-compare-slider="compareLayers"
          :is-embed="features.legend && !features.layerlist"
          @toggle-layer="toggleLayer"
          @set-layer-opacity="setLayerOpacity"
          @on-fit="(layer) => $refs.map.fit(layer)"
          @set-position="setPosition"
          @toggle-is-selectable="onToggleIsSelectable"
        />
      </div>
      <div class="bottom-center-panels">
        <CompareLayersSlider :map-id="mapId" :show-compare-layer-panel="compareLayers" />
      </div>
      <div class="bottom-right-panels" :class="{ 'bottom-panels-padding': compareLayers }">
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
import { DEFAULT_DRAWING_COLOR, DEFAULT_DRAWING_FONT_SIZE, DEFAULT_DRAWING_STROKE_WIDTH } from "@/constants/defaults";
import { useEditLayerStore } from "@/stores/edit_layer_store";
import AddFeaturePanel from "@/components/edit-layers/AddFeaturePanel.vue";
import EditFeaturePanel from "@/components/edit-layers/EditFeaturePanel.vue";
import { EditLayerMode } from "@/types/map";

const reverseGeocodingEndpoint = "https://api.pdok.nl/bzk/locatieserver/search/v3_1/reverse";

export default {
  name: "MapRenderer",
  components: {
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
    hideResetButton: {
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
      showAbout: false,
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
    };
  },
  computed: {
    EditLayerMode() {
      return EditLayerMode;
    },
    ...mapStores(useGlobalStore, useEditLayerStore),
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
    visibleLayers() {
      return this.layers.filter((l) => !l.is_base && l.is_visible);
    },
    regularLayers() {
      return this.layers.filter((l) => !l.is_base);
    },
    wmsWfsLayers() {
      return this.layers.filter((l) => !l.is_base && (l.source_type === "WMS" || l.source_type === "WMS_WFS"));
    },
    baseLayers() {
      return this.layers.filter((l) => l.is_base);
    },
    countOfLayersWithActiveFilters() {
      return this.mapStore ? this.mapStore.getActiveLayersWithFilterCount : 0;
    },
    countOfActiveSelectedFiltersForLayer() {
      return this.mapStore && this.settings.facets
        ? this.mapStore.getActiveSelectedItemCountPerFilterForLayer(this.settings.filterLayerId, this.settings.facets)
        : 0;
    },
  },
  watch: {
    initialPosition: {
      handler(value) {
        this.position = value;
      },
      deep: true,
    },
    visibleLayers: {
      handler(value) {
        this.editLayerStore.setVisibleLayers(value);
      },
      deep: true,
      immediate: true,
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
        // Store initial drawing features only once when they first load
        if (value && value.length > 0 && !this.initialDrawing) {
          this.initialDrawing = [...value];
        }
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
    features: {
      handler(value) {
        this.showAbout = value.showAbout ? value.showAbout : false;
      },
      deep: true,
    },
  },
  mounted() {
    window.addEventListener("resize", this.onResizeWindow);
    this.setViewportHeight();
    this.showAbout = this.features.showAbout ? this.features.showAbout : false;

    this.mapStore = useMapStore(this.mapId);

    // Store initial base layer ID
    const initialBaseLayer = this.layers.find((l) => l.is_base && l.is_visible);
    if (initialBaseLayer) {
      this.initialBaseLayerId = initialBaseLayer.id;
    }
  },
  emits: ["position-changed", "layers-changed", "update-user-settings"],
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
      this.editLayerStore.setHighlightedFeatureAndLayer(null);

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
          const features = data.features.map((feature) => new GeoJSON().readFeature(feature));
          this.highlightedFeatures = [...this.highlightedFeatures, ...features];

          /*
            If highlightedFeatureAndLayer is null and there is at least one highlighted feature,
            set it to the first highlighted feature along with its corresponding layer.
            This is necessary to enable edit and delete functionality for layers.

            Currently, if multiple features are highlighted, the edit and delete functionality
            only supports the first highlighted feature. If a user wants to edit a specific highlighted feature
            but has selected multiple features simultaneously,
            they will need to temporarily disable the layers containing other highlighted features.
           */
          if (!this.editLayerStore.highlightedFeatureAndLayer && features.length) {
            this.editLayerStore.setHighlightedFeatureAndLayer({ feature: features[0], layer: layer });
          }
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
    toggleAbout() {
      this.showAbout = !this.showAbout;
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
        case "Point":
        case "LineString":
        case "LinearRing":
        case "MultiPoint":
        case "MultiLineString":
        case "MultiPolygon":
        case "Circle":
          this.editLayerStore.setFeature(result.sketch);
          this.tool = "";
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
      if (layerId === this.initialBaseLayerId) {
        this.baseLayerChanged = !isVisible;
      }

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
    closeCompareLayerPanel() {
      this.showCompareLayerPanel = false;
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
