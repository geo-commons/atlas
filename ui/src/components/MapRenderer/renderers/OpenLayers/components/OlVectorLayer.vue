<template>
  <div v-if="false"></div>
</template>

<script>
import { toRaw } from "vue";
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
    features: {
      handler(features) {
        this.vectorSource.clear();
        this.vectorSource.addFeatures(features.map((feature) => toRaw(feature)));
      },
      deep: true,
    },
  },
  created() {
    this.vectorSource = new VectorSource();

    this.vectorLayer = new VectorLayer({
      name: this.name,
      source: this.vectorSource,
      style: toRaw(this.vectorStyle),
      visible: this.isVisible,
      opacity: this.opacity,
      zIndex: this.zIndex,
      properties: {
        selectable: this.selectable,
      },
    });

    this.vectorSource.addFeatures(this.features.map((feature) => toRaw(feature)));
    this.map.addLayer(this.vectorLayer);
  },
  unmounted() {
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
