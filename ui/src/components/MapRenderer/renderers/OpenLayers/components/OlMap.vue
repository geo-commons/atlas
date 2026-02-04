<template>
  <div
    ref="map"
    class="map"
    tabindex="0"
    role="application"
    aria-roledescription="map"
    aria-label="Interactieve kaart - gebruik de pijltjestoetsen om te navigeren, + en - om in en uit te zoomen"
  >
    <slot></slot>
    <div
      class="scale"
      :style="{ display: features.scale ? 'block' : 'none' }"
      :class="{ 'bottom-panels-padding': showCompareSlider }"
      @click="toggleScaleType"
    >
      <div ref="scale-line-container" :style="{ display: scaleType === 'LINE' ? 'block' : 'none' }" />
      <div class="scale-text" :style="{ display: scaleType === 'TEXT' ? 'block' : 'none' }">
        1 : {{ Math.round(scale).toLocaleString() }}
      </div>
    </div>
  </div>
</template>

<script>
import { toRaw } from "vue";
import Map from "ol/Map";
import ScaleLine from "ol/control/ScaleLine";
import { register } from "ol/proj/proj4";
import { getPointResolution } from "ol/proj";
import { getDefinitions } from "../../../../../utils/projections";
import DoubleClickZoom from "ol/interaction/DoubleClickZoom";
import DragPan from "ol/interaction/DragPan";
import KeyboardPan from "ol/interaction/KeyboardPan";
import KeyboardZoom from "ol/interaction/KeyboardZoom";
import MouseWheelZoom from "ol/interaction/MouseWheelZoom";
import PinchZoom from "ol/interaction/PinchZoom";

const DEFAULT_DPI = 25.4 / 0.28;

export default {
  name: "OlMap",
  provide() {
    return {
      map: toRaw(this.map),
    };
  },
  props: {
    features: Object,
    showCompareSlider: Boolean,
  },
  emits: ["set-position"],
  setup() {
    register(getDefinitions());
  },
  data() {
    return {
      map: new Map({
        controls: [],
        interactions: [
          new KeyboardPan(),
          new KeyboardZoom(),
          new DragPan(),
          new MouseWheelZoom(),
          new DoubleClickZoom(),
          new PinchZoom(),
        ],
      }),
      scaleType: "LINE",
      scale: 0,
    };
  },
  mounted() {
    this.map.setTarget(this.$refs["map"]);

    // show pointer on clickable features
    this.map.on("pointermove", (e) => {
      if (e.dragging) {
        return;
      }

      const pixel = this.map.getEventPixel(e.originalEvent);
      const hit = this.map.hasFeatureAtPixel(pixel, {
        layerFilter: (layer) => layer.get("selectable"),
      });

      this.map.getTarget().style.cursor = hit ? "pointer" : "";
    });

    this.map.on("moveend", () => {
      const view = this.map.getView();

      const resolution = getPointResolution(view.getProjection(), view.getResolution(), view.getCenter());

      const mpu = view.getProjection().getMetersPerUnit();
      const inchesPerMeter = 1000 / 25.4;
      this.scale = parseFloat(resolution.toString()) * mpu * inchesPerMeter * DEFAULT_DPI;

      this.$emit("set-position", {
        ...this.position,
        center: view.getCenter(),
        zoom: view.getZoom(),
        extent: view.calculateExtent(this.map.getSize()),
      });
    });

    this.scaleline = new ScaleLine({
      text: true,
      target: this.$refs["scale-line-container"],
      className: "scale-line",
    });

    this.map.addControl(this.scaleline);
  },
  methods: {
    toggleScaleType() {
      this.scaleType = this.scaleType === "LINE" ? "TEXT" : "LINE";
    },
    // id is the slug of a layer, we update the params to refresh the layer
    refreshLayer(id) {
      const layer = this.map
        .getLayers()
        .getArray()
        .find((layer) => layer.get("id") === id);

      if (layer) {
        layer.getSource().updateParams({ timestamp: Date.now() });
      } else {
        console.error("Could not retrieve layer with id", id);
      }
    },
  },
};
</script>

<style scoped>
.map {
  flex: 1 1 auto;
  width: 100%;
  height: 0;
}

.keyboard-user .map:focus {
  outline: none;
  position: relative;
}

.keyboard-user .map:focus::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  border: 3px solid var(--color-primary);
  pointer-events: none;
  z-index: 1000;
}

.map ::v-deep(.ol-attribution) {
  position: absolute;
  padding: 2px;
  background: rgba(255, 255, 255, 0.7);
  text-align: right;
  display: flex;
  flex-flow: row-reverse;
  align-items: center;
  bottom: 0;
  right: 0;
  border-radius: 4px 0 0;
}

.map ::v-deep(.ol-unselectable) {
  user-select: none;
}

.map ::v-deep(.ol-attribution.ol-uncollapsible) button {
  display: none;
}

.map ::v-deep(.ol-attribution) ul {
  margin: 0;
  padding: 1px 0.5em;
  color: #333;
  text-shadow: 0 0 2px #fff;
  font-size: 10px;
}

/* Make sure map fills window when viewers are enabled. */
.map.in-splitter {
  height: 100%;
}

.scale {
  position: absolute;
  right: calc(var(--padding-screen) * 2 + var(--width-button-normal));
  bottom: var(--padding-screen);
  background: rgba(255, 255, 255, 0.8);
  font-size: var(--font-size-tiny);
  font-weight: var(--font-weight-bold);
  color: black;
  user-select: none;
  cursor: pointer;
  z-index: 1;
}

.scale :deep(.scale-text) {
  height: 20px;
  line-height: 20px;
  padding: 0 4px;
}

.scale :deep(.scale-line-inner) {
  height: 20px;
  line-height: 20px;
  border: 2px solid black;
  border-top: none;
  text-align: center;
  will-change: contents, width;
  transition: all 0.25s ease;
}

@media (max-width: 640px) {
  .bottom-panels-padding {
    margin-bottom: 60px;
  }
}
</style>
