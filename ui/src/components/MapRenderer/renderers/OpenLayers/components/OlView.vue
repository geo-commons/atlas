<template>
  <div v-if="false"></div>
</template>

<script>
import Projection from "ol/proj/Projection";
import { getPointResolution } from "ol/proj";
import View from "ol/View";

const DEFAULT_DPI = 25.4 / 0.28;

const rdProjection = new Projection({
  code: "EPSG:28992",
  units: "m",
});

export default {
  name: "OlView",
  inject: ["map"],
  props: {
    position: Object,
    padding: Array,
    isVisible: Boolean,
    markerOnClick: Boolean,
    tool: String,
  },
  watch: {
    position(value, oldValue) {
      const view = this.map.getView();

      if (value.center != oldValue.center) {
        view.setCenter(value.center);
      }

      if (value.zoom != oldValue.zoom) {
        view.animate({
          zoom: value.zoom,
          duration: 250,
        });
      }
    },
    padding(value) {
      const view = this.map.getView();
      view.setProperties({ padding: value });
    },
  },
  mounted() {
    this.view = new View({
      projection: rdProjection,
      constrainResolution: true,
      enableRotation: false,
      center: this.position.center,
      zoom: this.position.zoom,
      padding: this.padding,
    });

    this.map.setView(this.view);

    this.map.on("moveend", () => {
      const view = this.map.getView();

      const resolution = getPointResolution(
        this.view.getProjection(),
        this.view.getResolution(),
        this.view.getCenter()
      );

      const mpu = this.view.getProjection().getMetersPerUnit();
      const inchesPerMeter = 1000 / 25.4;
      this.scale =
        parseFloat(resolution.toString()) * mpu * inchesPerMeter * DEFAULT_DPI;

      this.$emit("position-changed", {
        ...this.position,
        center: view.getCenter(),
        zoom: view.getZoom(),
        extent: view.calculateExtent(this.map.getSize()),
      });
    });

    this.map.on("singleclick", (e) => {
      if (this.tool !== "") {
        return;
      }

      if (this.markerOnClick) {
        this.$emit("position-changed", {
          ...this.position,
          marker: e.coordinate,
        });
      }
    });
  },
  methods: {
    fit(geometryOrExtent, options) {
      this.view.fit(geometryOrExtent, options);
    },
    centerOn(coordinates) {
      this.view.animate({ center: coordinates, duration: 100 });
    },
    adjustZoom(delta) {
      this.view.animate({ zoom: this.view.getZoom() + delta, duration: 100 });
    },
  },
};
</script>

<style scoped></style>
