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
    };
  },
  watch: {
    position(value, oldValue) {
      const view = this.map.getView();

      const centerChanged =
        !oldValue.center || value.center[0] !== oldValue.center[0] || value.center[1] !== oldValue.center[1];
      const zoomChanged = value.zoom !== oldValue.zoom;

      // Only animate if something actually changed
      if (centerChanged || zoomChanged) {
        const duration = value.animateFast ? 300 : 1500;

        // Cancel any existing animation before starting a new one
        view.cancelAnimations();
        this.isAnimating = true;

        // Create animation object with all changes
        const animation = {};
        if (centerChanged) {
          animation.center = value.center;
        }
        if (zoomChanged) {
          animation.zoom = value.zoom;
        }

        view.animate(
          {
            ...animation,
            duration: duration,
          },
          (completed) => {
            this.isAnimating = false;
            if (completed) {
              // Only emit completion if animation wasn't cancelled
              this.$emit("pan-animation-complete");
            }
          },
        );
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
