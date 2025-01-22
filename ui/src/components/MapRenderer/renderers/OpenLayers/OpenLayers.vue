<template>
  <ol-map ref="map" :features="features">
    <ol-view
      ref="view"
      :position="position"
      :padding="padding"
      :tool="tool"
      :marker-on-click="features.markerOnClick"
      @position-changed="onPositionChanged"
    />
    <ol-draw-interaction
      v-if="tool"
      :tool="tool"
      :layers="layers"
      :color="color"
      :stroke-width="strokeWidth"
      :font-size="fontSize"
      @draw-start="startUsingTool"
      @draw-end="toolUsed"
      @on-fit="onFit"
    />
    <ol-drag-zoom />
    <component
      :is="getComponent(layer.source_type)"
      v-for="layer in layers"
      :id="layer.id"
      :key="layer.id"
      :name="layer.name"
      :url="layer.url"
      :format="layer.format"
      :filters="filters"
      :is-visible="layer.is_visible === true"
      :is-selectable="layer.is_selectable === true"
      :send-token-with-request="layer.login_required && layer.source.authenticate && user && user.token ? true : false"
      :selected-features="selectedFeatures"
      :z-index="layer.is_base ? 0 : 1"
      :min-zoom="layer.zoom_min"
      :max-zoom="layer.zoom_max"
      :client-style="layer.client_style"
      :server-style="layer.server_style"
      :opacity="layer.opacity"
      @features-selected="featuresSelected"
    >
    </component>
    <ol-vector-layer
      v-if="mapArea"
      name="mapArea"
      :is-visible="true"
      :selectable="false"
      :vector-style="MAP_AREA_STYLE"
      :features="mapArea"
      :z-index="3"
    />
    <ol-vector-layer
      name="marker"
      :is-visible="true"
      :selectable="false"
      :vector-style="MARKER_STYLE"
      :features="markerFeatures"
      :z-index="3"
    />
    <ol-vector-layer
      name="geolocation"
      :selectable="false"
      :is-visible="true"
      :vector-style="GEOLOCATION_STYLE"
      :features="geolocationFeatures"
      :z-index="3"
    />
    <ol-vector-layer
      ref="selectedArea"
      name="selectedArea"
      :selectable="false"
      :is-visible="true"
      :vector-style="SELECTED_AREA_STYLE"
      :features="selectedAreaFeatures"
      :z-index="2"
    />
    <ol-vector-layer
      ref="highlightedSelection"
      name="highlightedSelection"
      :selectable="true"
      :is-visible="true"
      :vector-style="HIGHLIGHTED_SELECTION_STYLE"
      :features="highlightedFeatures"
      :z-index="2"
    />
    <ol-vector-layer
      ref="draw"
      name="draw"
      :selectable="true"
      :is-visible="true"
      :features="drawFeatures"
      :vector-style="DRAW_STYLE"
      :z-index="2"
    />
  </ol-map>
</template>

<script>
import { Circle, Fill, Icon, Stroke, Style, Text } from "ol/style";
import Feature from "ol/Feature";
import { Point } from "ol/geom";

import OlMap from "./components/OlMap";
import OlView from "./components/OlView";
import OlDrawInteraction from "./components/OlDrawInteraction";
import OlDragZoom from "./components/OlDragZoom";
import OlWmtsLayer from "./components/OlWmtsLayer";
import OlWmsLayer from "./components/OlWmsLayer";
import OlWfsLayer from "./components/OlWfsLayer";
import OlXyzLayer from "./components/OlXyzLayer";
import OlMvtLayer from "./components/OlMvtLayer";
import OlVectorLayer from "./components/OlVectorLayer";
import getMarkerIconUrl from "../../../../utils/generate-marker-icon-url";
import getLocationIconUrl from "../../../../utils/generate-location-icon-url";
import "ol/ol.css";
import { getFeatureFontSize, getFeatureRgba, getFeatureStrokeWidth } from "@/utils/feature-utils";
import { fetchLegendImage } from "@/utils/legend-utils";
import { printMapToPdf } from "@/utils/print-util";

const MARKER_STYLE = new Style({
  image: new Icon({
    src: getMarkerIconUrl("#0066FF", "#FFFFFF"),
    anchor: [0.55, 42],
    anchorXUnits: "fraction",
    anchorYUnits: "pixels",
  }),
});

const GEOLOCATION_STYLE = new Style({
  image: new Icon({
    src: getLocationIconUrl("#0066FF", "#FFFFFF"),
    anchor: [0.55, 42],
    anchorXUnits: "fraction",
    anchorYUnits: "pixels",
  }),
});

const MAP_AREA_STYLE = new Style({
  stroke: new Stroke({ color: "rgba(0, 102, 255, 1)", width: 2 }),
});

const SELECTED_AREA_STYLE = new Style({
  stroke: new Stroke({ color: "rgba(0, 102, 255, 1)" }),
  fill: new Fill({ color: "rgba(0, 102, 255, 0.2)" }),
});

const HIGHLIGHTED_SELECTION_STYLE = new Style({
  stroke: new Stroke({ color: "rgba(0, 102, 255, 1)", width: 5 }),
  fill: new Fill({ color: "rgba(0, 102, 255, 0.2)" }),
});

export default {
  name: "OpenLayers",
  components: {
    OlMap,
    OlView,
    OlDrawInteraction,
    OlDragZoom,
    OlWmtsLayer,
    OlWmsLayer,
    OlWfsLayer,
    OlXyzLayer,
    OlMvtLayer,
    OlVectorLayer,
  },
  props: {
    position: Object,
    layers: Array,
    tool: String,
    mapArea: Array,
    selectedArea: Object,
    user: Object,
    config: Object,
    features: Object,
    selectedFeatures: Array,
    highlightedFeatures: { type: Array, default: () => [] },
    drawFeatures: { type: Array, default: () => [] },
    filters: Object,
    padding: { type: Array, default: () => [0, 0, 0, 0] },
    color: Object,
    strokeWidth: Number,
    fontSize: Number,
  },
  emits: ["position-changed", "tool-used", "on-fit", "features-selected", "loading-print-to-pdf"],
  data() {
    return {
      undoRedoInteraction: null,
    };
  },
  computed: {
    DRAW_STYLE() {
      return (feature) =>
        new Style({
          image: feature.get("label")
            ? null
            : new Circle({
                radius: getFeatureStrokeWidth(feature, true),
                fill: new Fill({
                  color: getFeatureRgba(feature, 1), // color of points
                }),
              }),
          stroke: new Stroke({
            color: getFeatureRgba(feature, 1),
            width: getFeatureStrokeWidth(feature, false),
          }), // color of line
          fill: new Fill({
            color: getFeatureRgba(feature, 0.2),
          }), // fill of polygon (lower opacity part)
          text: new Text({
            text: feature.get("label")
              ? feature.get("label")
              : feature.get("xCoordinate") && feature.get("yCoordinate")
                ? `${+feature.get("xCoordinate").toFixed(2)}, ${+feature.get("yCoordinate").toFixed(2)}`
                : null,
            fill: new Fill({
              color: getFeatureRgba(feature, 1),
            }), // color of text
            textAlign: "left",
            offsetX:
              feature.get("xCoordinate") && feature.get("yCoordinate")
                ? getFeatureStrokeWidth(feature) > 3
                  ? 16
                  : 8
                : 0,
            font: `${getFeatureFontSize(feature)}px bold PT Sans, sans-serif`,
            stroke: new Stroke({
              color: getFeatureRgba(feature, 1),
              width: 1,
            }), // color of text
          }),
        });
    },
    markerFeatures() {
      if (!this.position.marker) {
        return [];
      }

      return [
        new Feature({
          geometry: new Point([this.position.marker[0], this.position.marker[1]]),
        }),
      ];
    },
    geolocationFeatures() {
      if (!this.position.geolocation) {
        return [];
      }

      return [
        new Feature({
          geometry: new Point([this.position.geolocation[0], this.position.geolocation[1]]),
        }),
      ];
    },
    selectedAreaFeatures() {
      if (!this.selectedArea) {
        return [];
      }

      return [new Feature({ geometry: this.selectedArea })];
    },
  },
  watch: {
    tool(tool) {
      if (tool) {
        return;
      }

      this.$refs.selectedArea.clear();
    },
  },
  created() {
    this.MAP_AREA_STYLE = MAP_AREA_STYLE;
    this.MARKER_STYLE = MARKER_STYLE;
    this.GEOLOCATION_STYLE = GEOLOCATION_STYLE;
    this.SELECTED_AREA_STYLE = SELECTED_AREA_STYLE;
    this.HIGHLIGHTED_SELECTION_STYLE = HIGHLIGHTED_SELECTION_STYLE;
  },
  methods: {
    fetchLegendImage,
    getComponent(sourceType) {
      switch (sourceType) {
        case "WMTS":
          return "ol-wmts-layer";
        case "WMS":
        case "WMS_WFS":
          return "ol-wms-layer";
        case "WFS":
          return "ol-wfs-layer";
        case "XYZ":
          return "ol-xyz-layer";
        case "MVT":
          return "ol-mvt-layer";
        default:
          return "ol-wms-layer";
      }
    },
    onPositionChanged(position) {
      this.$emit("position-changed", position);
    },
    getMarkerFeature(marker) {
      return new Feature({ geometry: new Point([marker[0], marker[1]]) });
    },
    startUsingTool() {
      this.$refs.selectedArea.clear();
    },
    toolUsed(result) {
      this.$emit("tool-used", result);
    },
    onFit(value) {
      this.$emit("on-fit", value);
    },
    fit(geometryOrExtent, options) {
      this.$refs.view.fit(geometryOrExtent, options);
    },
    featuresSelected(features) {
      this.$emit("features-selected", features);
    },
    async printToPdf(settings) {
      try {
        this.$emit("loading-print-to-pdf", true);
        // Wait for the promise to resolve
        await new Promise((resolve) => setTimeout(resolve, 500));
        await printMapToPdf(settings, this.$refs.map.map, this.layers, this.user, this.config, this.position);
      } catch (e) {
        console.error("Failed to print PDF:", e);
      } finally {
        this.$emit("loading-print-to-pdf", false);
      }
    },
  },
};
</script>

<style scoped>
.map :deep(.ol-tooltip) {
  position: relative;
  background: rgba(0, 0, 0, 0.5);
  border-radius: 4px;
  color: white;
  padding: 4px 8px;
  opacity: 0.7;
  white-space: nowrap;
  font-size: 12px;
  cursor: default;
  user-select: none;
}

.map :deep(.ol-tooltip-measure) {
  opacity: 1;
  font-weight: bold;
}

.map :deep(.ol-tooltip-static) {
  background-color: #000000;
  color: white;
  border: 1px solid white;
}

.map :deep(.ol-tooltip-measure:before),
.map :deep(.ol-tooltip-static:before) {
  border-top: 6px solid rgba(0, 0, 0, 0.5);
  border-right: 6px solid transparent;
  border-left: 6px solid transparent;
  content: "";
  position: absolute;
  bottom: -6px;
  margin-left: -7px;
  left: 50%;
}

.map :deep(.ol-tooltip-static:before) {
  border-top-color: #000000;
}

.map :deep(.ol-box) {
  box-sizing: border-box;
  border-radius: 2px;
  border: 1.5px solid #b3c5db;
  background-color: rgba(255, 255, 255, 0.4);
}
</style>
