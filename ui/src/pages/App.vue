<template>
  <div class="app" :class="{ showInfoPanel: showInfoPanel, showDataPanel }" :style="computedStyle">
    <header-menu v-if="!isEmbed && config.features.portal" />
    <div class="map-container">
      <div class="renderer-container">
        <PanoramaPanel class="panorama-panel" :position="position" :is-open="showPanoramaPanel" @toggle="togglePanoramaPanel" />
        <OpenLayersRenderer
          v-if="readyToRenderMap"
          ref="map"
          class="map"
          :position="position"
          :layers="layers"
          :tool="tool"
          :selected-area="selectedArea"
          :padding="mapPadding"
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
        @on-fit="(feature) => $refs.map.fit(feature, { maxZoom: 18 })"
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
      <div v-show="!showDataPanel || !showDataPanelFullScreen" class="ui-container">
        <div class="top-left-panels">
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
          <MorePanel v-if="!isEmbed && !showPanoramaPanel" :user="user" :show-disclaimer="config.show_disclaimer" @toggle-modal="toggleModal" />
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
          />
        </div>
        <div class="bottom-right-panels">
          <div
            v-if="!isEmbed && !showPanoramaPanel"
            class="bottom-right-buttons"
            :class="{
              isOpen: showBaseLayersPanel,
              showTogglePanorama: position.marker || showPanoramaPanel,
            }"
          >
            <button v-tippy="{ placement: 'left' }" class="iconbutton" content="Panorama" aria-label="Toon panorama" @click="togglePanoramaPanel">
              <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
                <path d="M0 0h24v24H0z" fill="none" />
                <path
                  d="M12 7C6.48 7 2 9.24 2 12c0 2.24 2.94 4.13 7 4.77V20l4-4-4-4v2.73c-3.15-.56-5-1.9-5-2.73 0-1.06 3.04-3 8-3s8 1.94 8 3c0 .73-1.46 1.89-4 2.53v2.05c3.53-.77 6-2.53 6-4.58 0-2.76-4.48-5-10-5z"
                />
              </svg>
            </button>
            <button
              v-tippy="{ placement: 'left' }"
              class="iconbutton"
              content="Basislagen"
              aria-label="Toon basislagen"
              :aria-expanded="showBaseLayersPanel.toString()"
              aria-controls="baseLayers"
              @click="toggleBaseLayersPanel"
            >
              <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
                <path d="M0 0h24v24H0V0z" fill="none" />
                <path
                  d="M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1 5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5zM10 5.47l4 1.4v11.66l-4-1.4V5.47zm-5 .99l3-1.01v11.7l-3 1.16V6.46zm14 11.08l-3 1.01V6.86l3-1.16v11.84z"
                />
              </svg>
            </button>
            <transition name="fade">
              <BaseLayersPanel v-if="showBaseLayersPanel" :layers="layers" @toggle-layer="toggleLayer" />
            </transition>
          </div>
          <GeoLocationButton @set-position="setPosition" />
          <ZoomPanel :position="position" @set-position="setPosition" />
        </div>
      </div>

      <transition name="fade">
        <EmbedModal v-if="modal === 'embed'" :layers="layers" :position="position" @toggle-modal="toggleModal" />
        <PrintModal v-if="modal === 'print'" @toggle-modal="toggleModal" @print-map-to-pdf="printMapToPdf" />
        <DrawingModal v-if="modal === 'drawing'" :layers="layers" :position="position" :drawing="drawing" @toggle-modal="toggleModal" />
      </transition>
      <AlertMessage :alert="alert" />
    </div>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import GeoJSON from "ol/format/GeoJSON";
import { mapState } from "vuex";
import { isMobile } from "../utils/helpers";
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
      modal: "",
      mapPadding: [0, 0, 0, 0],
    };
  },
  computed: mapState({
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
  watch: {
    position(value) {
      this.showInfoPanel = Boolean(value.marker);
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
    window.addEventListener("resize", this.onResizeWindow);
    this.setViewportHeight();

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
  destroyed() {
    window.removeEventListener("resize", this.onResizeWindow);
    clearInterval(this.fetchInterval);
  },
  methods: {
    onResizeWindow() {
      this.setViewportHeight();
    },
    setViewportHeight() {
      this.computedStyle["--vh"] = window.innerHeight / 100 + "px";
    },
    async setPosition(position) {
      this.$store.commit("setPosition", position);

      if (!position.marker) {
        return;
      }

      try {
        const result = await fetch(`${reverseGeocodingEndpoint}?X=${position.marker[0]}&Y=${position.marker[1]}&rows=1&distance=20`);
        const data = await result.json();

        if (!data.response.docs || data.response.docs.length === 0) {
          this.$store.commit("setSearchQuery", `(${Math.round(position.marker[0] * 100) / 100},${Math.round(position.marker[1] * 100) / 100})`);
          return;
        }

        const object = data.response.docs[0];
        this.$store.commit("setSearchQuery", object.weergavenaam);
      } catch (e) {
        console.error(e);
      }
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
    toggleInfoPanel() {
      this.showInfoPanel = !this.showInfoPanel;
    },
    togglePanoramaPanel() {
      this.showBaseLayersPanel = false;
      this.showPanoramaPanel = !this.showPanoramaPanel;
    },
    toggleBaseLayersPanel() {
      this.showPanoramaPanel = false;
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
        `${basePath[1]}@${x},${y},${zoom}z/layers=${layers}/base=${baseLayer.length > 0 ? baseLayer[0] : ""}/drawing=${
          this.drawing ? this.drawing : ""
        }`
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

      if (!isMobile() && this.showDataPanel) {
        this.$set(this.mapPadding, 3, window.innerWidth * 0.5);
      } else {
        this.$set(this.mapPadding, 3, 0);
      }
    },
    toggleDataPanelFullScreen() {
      this.showDataPanelFullScreen = !this.showDataPanelFullScreen;
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
    padding: 0 20px;
  }

  .section {
    padding: 32px 0;
  }
}

@media (min-width: 576px) {
  .container {
    padding: 0 32px;
  }

  .section {
    padding: 40px 0;
  }
}

@media (max-width: 575px) {
  .container {
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
  .top-right-panels {
    top: var(--padding-screen);
  }

  .showDataPanel .top-left-panels {
    display: none;
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
  height: var(--width-button-normal);
  transition: height 0.1s ease, border-radius 0.1s;
  overflow: hidden;
}

.bottom-right-buttons.isOpen {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.bottom-right-buttons.showTogglePanorama {
  height: calc(var(--width-button-normal) * 2 + 1px);
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
