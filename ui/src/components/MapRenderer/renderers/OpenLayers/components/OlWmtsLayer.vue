<template>
  <div v-if="false"></div>
</template>

<script>
import TileLayer from "ol/layer/Tile";
import Projection from "ol/proj/Projection";
import WMTSCapabilities from "ol/format/WMTSCapabilities";
import WMTSSource, { optionsFromCapabilities } from "ol/source/WMTS";

const rdProjection = new Projection({
  code: "EPSG:28992",
  units: "m",
});

export default {
  name: "WmtsLayer",
  inject: ["map"],
  props: {
    name: String,
    url: String,
    layer: String,
    isVisible: Boolean,
    opacity: Number,
    serverStyle: String,
    zIndex: Number,
    format: String,
    minZoom: Number,
    maxZoom: Number,
  },
  watch: {
    url(value) {
      this.source.set("url", value);
    },
    name(value) {
      this.tileLayer.set("name", value);
    },
    isVisible(value) {
      this.tileLayer.set("visible", value);

      if (value && !this.tileLayer.getSource()) {
        this.setSource();
      }
    },
    opacity(value) {
      this.tileLayer.set("opacity", value);
    },
  },
  created() {
    this.tileLayer = new TileLayer({
      name: this.name,
      visible: this.isVisible,
      opacity: this.opacity,
      source: null,
      zIndex: this.zIndex,
      minZoom: this.minZoom ? this.minZoom - 1 : undefined,
      maxZoom: this.maxZoom ? this.maxZoom : undefined,
    });

    this.map.addLayer(this.tileLayer);

    if (this.isVisible) {
      this.setSource();
    }
  },
  destroyed() {
    this.map.removeLayer(this.tileLayer);
  },
  methods: {
    async setSource() {
      const response = await fetch(
        `${this.url}?REQUEST=GetCapabilities&service=wmts`
      );
      const body = await response.text();
      const caps = new WMTSCapabilities().read(body);
      const wmtsSource = new WMTSSource(
        optionsFromCapabilities(caps, {
          layer: this.name,
          matrixSet: "EPSG:28992",
          projection: rdProjection,
          format: this.format,
          crossOrigin: "anonymous",
          style: this.serverStyle ? this.serverStyle : null,
        })
      );

      this.tileLayer.setSource(wmtsSource);
    },
  },
};
</script>

<style scoped></style>
