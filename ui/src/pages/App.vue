<template>
  <div class="app" :class="{ showDataPanel, showInfoPanel }" :style="computedStyle">
    <header-menu v-if="!isEmbed && config.features.portal" />
    <div ref="mapContainer" class="map-container">
      <div class="renderer-container">
        <PanoramaPanel
          class="panorama-panel"
          :position="position"
          :is-open="showPanoramaPanel"
          @toggle="togglePanoramaPanel"
        />
        <OpenLayersRenderer
          v-if="readyToRenderMap"
          ref="map"
          class="map"
          :position="position"
          :layers="layers"
          :tool="tool"
          :selected-area="selectedArea"
          :filters="filters"
          :highlighted-features="highlightedFeatures"
          :padding="mapPadding"
          :map-area="mapArea"
          :user="user"
          :features="{ scale: true, markerOnClick: true }"
          :draw-features="drawFeatures"
          :drawing="drawing"
          @position-changed="setPosition"
          @tool-used="toolUsed"
        />
      </div>
      <PointInfoPanel
        v-if="!showPanoramaPanel"
        :layers="layers"
        :position="position"
        :show-panel="!showDataPanel && showInfoPanel"
        :user="user"
        @set-position="setPosition"
        @on-fit="(feature) => $refs.map.fit(feature, { maxZoom: 19 })"
        @expanded-info-panel="toggleInfoPanel"
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
            v-if="!showPanoramaPanel"
            :position="position"
            :layers="layers"
            :features="{ dataPanel: true }"
            @set-position="setPosition"
            @toggle-data-panel="toggleDataPanel"
          />
        </div>

        <div class="top-right-panels">
          <ToolsPanel
            v-if="!isEmbed && !showPanoramaPanel"
            :tool="tool"
            :user="user"
            :draw-features="drawFeatures"
            :config="config"
            @set-tool="setTool"
            @set-selected-area="setSelectedArea"
            @drawing-saved="drawingSaved"
            @clear-draw="() => (drawFeatures = [])"
          />
          <MorePanel
            v-if="!isEmbed && !showPanoramaPanel"
            :user="user"
            :show-disclaimer="config.show_disclaimer"
            @toggle-modal="toggleModal"
          />
        </div>
        <div class="bottom-left-panels">
          <LayersPanel
            v-if="!showPanoramaPanel"
            :is-embed="isEmbed"
            :layers="layers"
            :position="position"
            :user="user"
            :initially-show-layer-list="initiallyShowLayerList"
            @toggle-layer="toggleLayer"
            @set-layer-opacity="setLayerOpacity"
            @on-fit="(layer) => $refs.map.fit(layer)"
            @set-position="setPosition"
          />
        </div>
        <div class="bottom-right-panels">
          <div
            v-if="!isEmbed"
            class="bottom-right-buttons"
            :class="{
              isOpen: showBaseLayersPanel,
            }"
          >
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
          <div
            v-if="!isEmbed && (panoramaViewers.length > 0 || obliqueViewers.length > 0)"
            class="bottom-right-buttons"
          >
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
          <GeoLocationButton @set-position="setPosition" />
          <ZoomPanel :position="position" @set-position="setPosition" />
        </div>
      </div>

      <transition name="fade">
        <EmbedModal v-if="modal === 'embed'" :layers="layers" :position="position" @toggle-modal="toggleModal" />
      </transition>
      <transition name="fade">
        <PrintModal v-if="modal === 'print'" @toggle-modal="toggleModal" @print-map-to-pdf="printMapToPdf" />
      </transition>
      <transition name="fade">
        <DrawingModal
          v-if="modal === 'drawing'"
          :layers="layers"
          :position="position"
          :drawing="drawing"
          @toggle-modal="toggleModal"
        />
      </transition>
      <AlertMessage :alert="alert" />
    </div>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import GeoJSON from "ol/format/GeoJSON";
import nunjucks from "nunjucks";
import { register } from "ol/proj/proj4";
import TileWMS from "ol/source/TileWMS";
import View from "ol/View";
import { mapState } from "vuex";
import { getDefinitions } from "../utils/projections";
import HeaderMenu from "../components/HeaderMenu";
import AlertMessage from "../components/AlertMessage";
import BaseLayersPanel from "../components/BaseLayersPanel";
import DataPanel from "../components/DataPanel";
import EmbedModal from "../components/EmbedModal";
import PrintModal from "../components/PrintModal";
import DrawingModal from "../components/DrawingModal";
import LayersPanel from "../components/LayersPanel";
import OpenLayersRenderer from "../components/MapRenderer/renderers/OpenLayers/OpenLayers";
import ToolsPanel from "../components/ToolsPanel";
import MorePanel from "../components/MorePanel";
import PanoramaPanel from "../components/PanoramaPanel";
import PointInfoPanel from "../components/PointInfoPanel";
import SearchPanel from "../components/SearchPanel";
import ZoomPanel from "../components/ZoomPanel";
import GeoLocationButton from "../components/GeoLocationButton";
import { isMobile } from "@/utils/helpers";
import { transform } from "ol/proj";
import MapIcon from "../assets/icons/map-icon.svg";
import PanoramaIcon from "../assets/icons/panorama-icon.svg";
import ObliqueIcon from "../assets/icons/oblique-icon.svg";

// Register EPSG:28992 projection
register(getDefinitions());

nunjucks.configure({ autoescaping: true });

const reverseGeocodingEndpoint = "https://api.pdok.nl/bzk/locatieserver/search/v3_1/reverse";

export default {
  name: "App",
  components: {
    HeaderMenu,
    AlertMessage,
    BaseLayersPanel,
    DataPanel,
    EmbedModal,
    PrintModal,
    DrawingModal,
    LayersPanel,
    OpenLayersRenderer,
    ToolsPanel,
    MorePanel,
    PanoramaPanel,
    PointInfoPanel,
    SearchPanel,
    ZoomPanel,
    GeoLocationButton,
    MapIcon,
    PanoramaIcon,
    ObliqueIcon,
  },
  data() {
    return {
      readyToRenderMap: false,
      showInfoPanel: Boolean(this.position && this.position.marker),
      showPanoramaPanel: false,
      showBaseLayersPanel: false,
      showDataPanel: false,
      showDataPanelFullScreen: false,
      computedStyle: { "--color-primary": "#0066FF" },
      drawFeatures: [],
      highlightedFeatures: [],
      modal: "",
      filters: {},
      mapPadding: [0, 0, 0, 0],
      infoPanelExpanded: false,
    };
  },
  computed: {
    ...mapState({
      isEmbed: (state) => state.isEmbed,
      alert: (state) => state.alert,
      position: (state) => state.position,
      layers: (state) => state.layers,
      tool: (state) => state.tool,
      user: (state) => state.user,
      config: (state) => state.config,
      selectedArea: (state) => state.selectedArea,
      initiallyShowLayerList: (state) => state.initiallyShowLayerList,
      drawing: (state) => state.drawing,
    }),
    panoramaViewers: function () {
      return this.config.viewers.filter((v) => !v.is_oblique);
    },
    obliqueViewers: function () {
      return this.config.viewers.filter((v) => v.is_oblique);
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
    mapArea() {
      if (!this.config.map_area) {
        return;
      }

      const geojsonFormat = new GeoJSON();
      return geojsonFormat.readFeatures(this.config.map_area);
    },
  },
  watch: {
    position(value) {
      // Toggle info panel based on if there is a marker present.
      this.showInfoPanel = Boolean(value.marker);

      if (this.showInfoPanel) {
        this.setWindowInnerWidth();
      }

      this.pushHistoryState();
    },
    layers() {
      this.pushHistoryState();
    },
    drawing() {
      this.pushHistoryState();
    },
  },
  created() {
    if (this.drawing) {
      this.fetchDrawing();
    }

    if (!this.user) {
      this.readyToRenderMap = true;
      return;
    }

    this.fetchAccessToken();

    this.fetchInterval = setInterval(() => {
      this.fetchAccessToken();
    }, 1000 * 60 * 5); // every 5 minutes
  },
  mounted() {
    window.addEventListener("resize", this.onResizeWindow);
    this.setViewportHeight();
  },
  destroyed() {
    window.removeEventListener("resize", this.onResizeWindow);
    clearInterval(this.fetchInterval);
  },
  methods: {
    onResizeWindow() {
      this.setViewportHeight();
    },
    setViewportHeight() {
      this.computedStyle["--vh"] = this.$refs.mapContainer.clientHeight / 100 + "px";
    },
    async setPosition(position) {
      this.$store.commit("setPosition", position);

      if (!position.marker) {
        this.highlightedFeatures = [];
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
    toggleLayer(values) {
      this.$store.commit("toggleLayer", values);
    },
    setLayerOpacity(values) {
      this.$store.commit("setLayerOpacity", values);
    },
    setTool(tool) {
      this.$store.commit("setTool", tool);
    },
    setSelectedArea(selectedArea) {
      this.$store.commit("setSelectedArea", selectedArea);
    },
    toolUsed(result) {
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
    togglePanoramaPanel() {
      this.showBaseLayersPanel = false;
      this.showPanoramaPanel = !this.showPanoramaPanel;
    },
    toggleBaseLayersPanel() {
      this.showBaseLayersPanel = !this.showBaseLayersPanel;
    },
    pushHistoryState() {
      const basePath = /(.*?)(@|$)/.exec(window.location.pathname);

      const x = encodeURIComponent(this.position.center[0].toFixed(2));
      const y = encodeURIComponent(this.position.center[1].toFixed(2));
      const zoom = encodeURIComponent(this.position.zoom);

      const layers = this.layers
        .filter((l) => l.is_visible && !l.is_base)
        .map((l) => l.id)
        .join(",");

      const baseLayer = this.layers.filter((l) => l.is_visible && l.is_base).map((l) => l.id);

      window.history.replaceState(
        {},
        "",
        `${basePath[1]}@${x},${y},${Math.round(zoom * 100) / 100}z/layers=${layers}/base=${
          baseLayer.length > 0 ? baseLayer[0] : ""
        }/drawing=${this.drawing ? this.drawing : ""}`
      );
    },
    toggleModal(modal) {
      this.modal = modal;
    },
    printMapToPdf(settings) {
      this.$refs.map.printToPdf(settings);
    },
    toggleDataPanel() {
      this.showDataPanel = !this.showDataPanel;
      if (!this.showDataPanel) {
        this.$store.commit("setSelectedArea", null);
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
    async fetchAccessToken() {
      const response = await fetch("/atlas/api/v1/token", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (!response.ok) {
        this.readyToRenderMap = true;
        return false;
      }

      const data = await response.json();
      this.$store.commit("setUser", {
        ...this.user,
        token: data.token,
      });

      this.readyToRenderMap = true;
    },
    async fetchDrawing() {
      const response = await fetch(`/atlas/api/v1/drawings/${this.drawing}/`);
      if (!response.ok) {
        return false;
      }

      const data = await response.json();

      const geojsonFormat = new GeoJSON();
      this.drawFeatures = data.features.map((feature) => geojsonFormat.readFeature(feature));
    },
    drawingSaved(id) {
      this.$store.commit("setDrawing", id);
      this.modal = "drawing";
    },
  },
};
</script>

<!-- Include multiselect -->
<style src="vue-multiselect/dist/vue-multiselect.min.css" />
<style>
@import "../assets/styles/main.css";
</style>
<style scoped>
.app {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}

.map-container {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  overflow: hidden;
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
  .container {
    flex-direction: column;
  }
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

.panorama-panel {
  flex: 0 1 auto;
}

.map {
  flex: 1 1 auto;
  height: 0; /* fixes incorrect display of .ol-viewport on Safari 13.1 */
}

.bottom-left-panels {
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
  position: absolute;
  bottom: var(--padding-screen);
  right: var(--padding-screen);
  display: flex;
  flex-direction: column;
}

.bottom-right-panels > *:not(:last-child) {
  margin-bottom: 12px;
}

.bottom-right-buttons {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  background: white;
  border-radius: var(--radius-normal);
  overflow: hidden;
  box-shadow: var(--shadow-normal);
  transition: height 0.1s ease, border-radius 0.1s;
}

.bottom-right-buttons.isOpen {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
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
