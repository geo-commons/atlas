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
  data() {
    return {
      isAnimating: false,
      scale: null,
    };
  },
  watch: {
    position(value, oldValue) {
      const view = this.map.getView();

      // Cancel any ongoing animations before starting new ones
      if (this.isAnimating) {
        view.cancelAnimations();
      }

      // Handle center changes
      if (value.center && (!oldValue || value.center !== oldValue.center)) {
        if (value.animateFast === true) {
          // Fast animated center change (300ms)
          this.isAnimating = true;
          view.animate(
            {
              center: value.center,
              duration: 300,
            },
            () => {
              this.isAnimating = false;
              this.$emit("pan-animation-complete");
            },
          );
        } else if (value.animateFast === false) {
          // Direct center change (no animation)
          view.setCenter(value.center);
        } else {
          // Default animated center change (1000ms)
          this.isAnimating = true;
          view.animate(
            {
              center: value.center,
              duration: 1000,
            },
            () => {
              this.isAnimating = false;
              this.$emit("pan-animation-complete");
            },
          );
        }
      }

      // Handle zoom changes
      if (value.zoom && (!oldValue || value.zoom !== oldValue.zoom)) {
        if (value.animateFast === true) {
          // Fast animated zoom change (300ms)
          this.isAnimating = true;
          view.animate(
            {
              zoom: value.zoom,
              duration: 300,
            },
            () => {
              this.isAnimating = false;
            },
          );
        } else if (value.animateFast === false) {
          // Direct zoom change (no animation)
          view.setZoom(value.zoom);
        } else {
          // Default animated zoom change (1000ms)
          this.isAnimating = true;
          view.animate(
            {
              zoom: value.zoom,
              duration: 1000,
            },
            () => {
              this.isAnimating = false;
            },
          );
        }
      }
    },
    padding: {
      handler(value) {
        const view = this.map.getView();
        view.setProperties({ padding: value });
      },
      deep: true,
    },
  },
  mounted() {
    this.view = new View({
      projection: rdProjection,
      enableRotation: false,
      center: this.position.center,
      zoom: this.position.zoom,
      padding: this.padding,
      minZoom: 1,
      maxZoom: 28,
    });

    this.map.setView(this.view);

    this.map.on("moveend", () => {
      const view = this.map.getView();

      const resolution = getPointResolution(
        this.view.getProjection(),
        this.view.getResolution(),
        this.view.getCenter(),
      );

      const mpu = this.view.getProjection().getMetersPerUnit();
      const inchesPerMeter = 1000 / 25.4;
      this.scale = parseFloat(resolution.toString()) * mpu * inchesPerMeter * DEFAULT_DPI;

      this.$emit("position-changed", {
        ...this.position,
        center: view.getCenter(),
        zoom: view.getZoom(),
        extent: view.calculateExtent(this.map.getSize()),
        flyTo: false, // reset fly to
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
    cancelAnimation() {
      if (this.isAnimating) {
        this.view.cancelAnimations();
        this.isAnimating = false;
      }
    },
  },
};
</script>

<style scoped></style>
