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
      currentAnimation: null,
    };
  },
  watch: {
    position(value, oldValue) {
      const view = this.map.getView();

      if (value.center !== oldValue.center) {
        if (value.animateFast) {
          // Cancel any existing animation before starting new one
          if (this.currentAnimation) {
            this.currentAnimation.cancel();
          }

          this.currentAnimation = view.animate(
            {
              center: value.center,
              duration: 300,
            },
            (completed) => {
              this.currentAnimation = null;
              if (completed) {
                // Only emit completion if animation wasn't cancelled
                this.$emit("pan-animation-complete");
              }
            },
          );
        } else {
          view.animate({
            center: value.center,
            duration: 1500,
          });
        }
      }

      if (value.zoom !== oldValue.zoom) {
        view.animate({
          zoom: value.zoom,
          duration: value.animateFast ? 300 : 1500,
        });
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
      if (this.currentAnimation) {
        this.currentAnimation.cancel();
        this.currentAnimation = null;
      }
    },
  },
};
</script>

<style scoped></style>
