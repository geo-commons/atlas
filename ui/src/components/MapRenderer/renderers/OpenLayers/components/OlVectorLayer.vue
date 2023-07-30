<template>
  <div v-if="false"></div>
</template>

<script>
import VectorLayer from "ol/layer/Vector";
import VectorSource from "ol/source/Vector";

export default {
  name: "VectorLayer",
  inject: ["map"],
  props: {
    name: String,
    vectorStyle: [Object, Function],
    features: Array,
    selectable: Boolean,
    isVisible: Boolean,
    opacity: Number,
    zIndex: Number,
  },
  watch: {
    features(features) {
      this.vectorSource.clear();
      this.vectorSource.addFeatures(features);
    },
  },
  created() {
    this.vectorSource = new VectorSource();

    this.vectorLayer = new VectorLayer({
      name: this.name,
      source: this.vectorSource,
      style: this.vectorStyle,
      visible: this.isVisible,
      opacity: this.opacity,
      zIndex: this.zIndex,
      properties: {
        selectable: this.selectable,
      },
    });

    this.vectorSource.addFeatures(this.features);
    this.map.addLayer(this.vectorLayer);
  },
  destroyed() {
    this.map.removeLayer(this.vectorLayer);
  },
  methods: {
    clear() {
      this.vectorSource.clear();
    },
  },
};
</script>

<style scoped></style>
