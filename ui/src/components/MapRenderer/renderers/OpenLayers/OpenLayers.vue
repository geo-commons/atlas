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
      @draw-start="startUsingTool"
      @draw-end="toolUsed"
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
      :send-token-with-request="
        layer.login_required && layer.source.authenticate && user && user.token
          ? true
          : false
      "
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
      :vector-style="DRAW_STYLE"
      :features="drawFeatures"
      :z-index="2"
    />
  </ol-map>
</template>

<script>
import { Icon, Circle, Style, Fill, Stroke, Text } from "ol/style";
import Feature from "ol/Feature";
import { Point } from "ol/geom";
import { jsPDF } from "jspdf";
import html2canvas from "html2canvas";

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

const SELECTED_AREA_STYLE = new Style({
  stroke: new Stroke({ color: "rgba(0, 102, 255, 1)" }),
  fill: new Fill({ color: "rgba(0, 102, 255, 0.2)" }),
});

const HIGHLIGHTED_SELECTION_STYLE = new Style({
  stroke: new Stroke({ color: "rgba(0, 102, 255, 1)", width: 5 }),
  fill: new Fill({ color: "rgba(0, 102, 255, 0.2)" }),
});

const DRAW_STYLE = (feature) =>
  new Style({
    image: feature.get("label")
      ? null
      : new Circle({
          radius: 8,
          fill: new Fill({
            color: "rgba(0, 102, 255, 1)",
          }),
        }),
    stroke: new Stroke({ color: "rgba(0, 102, 255, 1)", width: 5 }),
    fill: new Fill({ color: "rgba(0, 102, 255, 0.2)" }),
    text: new Text({
      text: feature.get("label"),
      fill: new Fill({ color: "rgba(0, 102, 255, 1)" }),
      font: "22px bold PT Sans, sans-serif",
      stroke: new Stroke({ color: "rgba(0, 102, 255, 1)", width: 1 }),
    }),
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
    selectedArea: Object,
    user: Object,
    features: Object,
    selectedFeatures: Array,
    highlightedFeatures: { type: Array, default: () => [] },
    drawFeatures: { type: Array, default: () => [] },
    filters: Object,
    padding: { type: Array, default: () => [0, 0, 0, 0] },
  },
  computed: {
    markerFeatures() {
      if (!this.position.marker) {
        return [];
      }

      return [
        new Feature({
          geometry: new Point([
            this.position.marker[0],
            this.position.marker[1],
          ]),
        }),
      ];
    },
    geolocationFeatures() {
      if (!this.position.geolocation) {
        return [];
      }

      return [
        new Feature({
          geometry: new Point([
            this.position.geolocation[0],
            this.position.geolocation[1],
          ]),
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
    drawFeatures(features) {
      this.$emit("features-drawn", features);
    },
  },
  created() {
    this.MARKER_STYLE = MARKER_STYLE;
    this.GEOLOCATION_STYLE = GEOLOCATION_STYLE;
    this.SELECTED_AREA_STYLE = SELECTED_AREA_STYLE;
    this.HIGHLIGHTED_SELECTION_STYLE = HIGHLIGHTED_SELECTION_STYLE;
    this.DRAW_STYLE = DRAW_STYLE;
  },
  methods: {
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
    fit(geometryOrExtent, options) {
      this.$refs.view.fit(geometryOrExtent, options);
    },
    featuresSelected(features) {
      this.$emit("features-selected", features);
    },
    printToPdf(settings) {
      const margin = 0;

      const dims = {
        a0: [1189, 841],
        a1: [841, 594],
        a2: [594, 420],
        a3: [420, 297],
        a4: [297, 210],
      };

      const resolution = 150;

      let dim = dims[settings.format].map((d) => d - margin * 2);
      if (settings.orientation === "portrait") {
        dim = dim.reverse();
      }

      const map = this.$refs.map.map;
      const view = map.getView();

      const width = Math.round((dim[0] * resolution) / 25.4);
      const height = Math.round((dim[1] * resolution) / 25.4);
      const size = map.getSize();
      const viewResolution = view.getResolution();

      map.once("rendercomplete", function () {
        const mapCanvas = document.createElement("canvas");
        mapCanvas.width = width;
        mapCanvas.height = height;
        const mapContext = mapCanvas.getContext("2d");
        Array.prototype.forEach.call(
          document.querySelectorAll(".ol-layer canvas"),
          function (canvas) {
            if (canvas.width > 0) {
              mapContext.globalAlpha = 1;
              const transform = canvas.style.transform;
              // Get the transform parameters from the style's transform matrix
              const matrix = transform
                .match(/^matrix\(([^(]*)\)$/)[1]
                .split(",")
                .map(Number);
              // Apply the transform to the export map context
              CanvasRenderingContext2D.prototype.setTransform.apply(
                mapContext,
                matrix
              );
              mapContext.drawImage(canvas, 0, 0);
            }
          }
        );

        mapContext.globalAlpha = 1;
        mapContext.setTransform(1, 0, 0, 1, 0, 0);

        html2canvas(document.querySelector(".scale")).then((scale) => {
          mapCanvas.toBlob((blob) => {
            const url = window.URL || window.webkitURL;
            const imgSrc = url.createObjectURL(blob);

            const img = new Image();
            img.src = imgSrc;

            const pdf = new jsPDF(
              settings.orientation,
              undefined,
              settings.format
            );

            pdf.addImage(img, "JPEG", margin, margin, dim[0], dim[1]);

            pdf.setFontSize(16);
            pdf.text(10, 10, settings.title);
            pdf.setFontSize(12);

            if (settings.showDateTime) {
              pdf.text(10, 15, new Date().toLocaleString());
            }

            pdf.text(10, 20, settings.remarks);

            if (settings.showLegend) {
              const legends = document.getElementsByClassName("legend");
              for (let i = 0; i < legends.length; i++) {
                pdf.addImage(
                  legends[i],
                  "JPEG",
                  dim[0] - legends[i].width / 5 - 5,
                  5,
                  legends[i].width / 5,
                  legends[i].height / 5
                );
              }
            }

            if (settings.showScale) {
              pdf.addImage(
                scale.toDataURL(),
                "JPEG",
                10,
                dim[1] - 10,
                scale.width / 5,
                scale.height / 5
              );
            }

            pdf.save(`atlas-${new Date().toISOString()}.pdf`);

            map.setSize(size);
            view.setResolution(viewResolution);
            document.body.style.cursor = "auto";
          });
        });
      });

      // Set print size
      const printSize = [width, height];
      map.setSize(printSize);
      const scaling = Math.min(width / size[0], height / size[1]);
      view.setResolution(viewResolution / scaling);
    },
  },
};
</script>

<style scoped>
.map >>> .ol-tooltip {
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

.map >>> .ol-tooltip-measure {
  opacity: 1;
  font-weight: bold;
}

.map >>> .ol-tooltip-static {
  background-color: #000000;
  color: white;
  border: 1px solid white;
}

.map >>> .ol-tooltip-measure:before,
.map >>> .ol-tooltip-static:before {
  border-top: 6px solid rgba(0, 0, 0, 0.5);
  border-right: 6px solid transparent;
  border-left: 6px solid transparent;
  content: "";
  position: absolute;
  bottom: -6px;
  margin-left: -7px;
  left: 50%;
}

.map >>> .ol-tooltip-static:before {
  border-top-color: #000000;
}

.map >>> .ol-box {
  box-sizing: border-box;
  border-radius: 2px;
  border: 1.5px solid #b3c5db;
  background-color: rgba(255, 255, 255, 0.4);
}
</style>
