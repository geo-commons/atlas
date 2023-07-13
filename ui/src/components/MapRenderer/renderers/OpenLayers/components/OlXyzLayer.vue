<template>
  <div v-if="false"></div>
</template>

<script>
import TileLayer from "ol/layer/Tile";
import Projection from "ol/proj/Projection";
import XYZSource from "ol/source/XYZ";

const rdProjection = new Projection({
  code: "EPSG:28992",
  units: "m",
});

export default {
  name: "OlXyzLayer",
  inject: ["map"],
  props: {
    name: String,
    url: String,
    layer: String,
    isVisible: Boolean,
    opacity: Number,
    zIndex: Number,
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
      zIndex: this.zIndex,
      source: new XYZSource({
        url: this.url,
        projection: rdProjection,
        minZoom: this.minZoom ? this.minZoom - 1 : undefined,
        maxZoom: this.maxZoom ? this.maxZoom : undefined,
      }),
    });

    this.map.addLayer(this.tileLayer);
  },
  destroyed() {
    this.map.removeLayer(this.tileLayer);
  },
};
</script>

<style scoped></style>
