<template>
  <div v-if="false"></div>
</template>

<script>
import constructDraw from "../../../../../utils/draw";
import { fromCircle } from "ol/geom/Polygon";

export default {
  name: "OlDrawInteraction",
  inject: ["map"],
  props: {
    layers: Array,
    tool: String,
    color: Object,
    strokeWidth: Number,
    fontSize: Number,
  },
  emits: ["draw-start", "draw-end", "on-fit"],
  created() {
    if (this.tool !== "SELECT_FEATURE") {
      const onDrawStart = () => {
        this.$emit("draw-start");
      };

      const onDrawEnd = (sketch) => {
        const geometry = sketch.getGeometry();
        if (this.tool === "SELECT_CIRCLE") {
          sketch.setGeometry(fromCircle(geometry));
        }

        this.$emit("draw-end", { tool: this.tool, sketch });

        if (this.tool === "SELECT_CIRCLE" || this.tool === "SELECT_AREA") {
          this.$emit("on-fit", geometry.getExtent());
        }
      };

      this.draw = constructDraw(
        this.tool,
        this.map,
        onDrawStart,
        onDrawEnd,
        this.color,
        this.strokeWidth,
        this.fontSize,
      );
      this.map.addInteraction(this.draw);
    }
  },
  unmounted() {
    if (this.tool !== "SELECT_FEATURE") {
      this.map.removeOverlay(this.draw.measureTooltip);
      this.map.removeInteraction(this.draw);
    }
  },
};
</script>
