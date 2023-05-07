<template>
  <div v-if="false"></div>
</template>

<script>
import Circle from "ol/geom/Circle";
import { fromCircle } from "ol/geom/Polygon";
import constructDraw from "../../../../../utils/draw";

export default {
  name: "OlDrawInteraction",
  inject: ["map"],
  props: {
    layers: Array,
    tool: String,
  },
  watch: {
    tool(tool) {
      this.map.removeInteraction(this.draw);

      const onDrawStart = () => {
        this.$emit("draw-start");
      };

      const onDrawEnd = (sketch) => {
        const geometry = sketch.getGeometry();
        if (geometry instanceof Circle) {
          sketch.setGeometry(fromCircle(geometry));
        }

        this.$emit("draw-end", { tool: tool, sketch });
      };

      this.draw = constructDraw(tool, this.map, onDrawStart, onDrawEnd);
      this.map.addInteraction(this.draw);
    },
  },
  created() {
    const onDrawStart = () => {
      this.$emit("draw-start");
    };

    const onDrawEnd = (sketch) => {
      this.$emit("draw-end", { tool: this.tool, sketch });
    };

    this.draw = constructDraw(this.tool, this.map, onDrawStart, onDrawEnd);
    this.map.addInteraction(this.draw);
  },
  destroyed() {
    this.map.removeOverlay(this.draw.measureTooltip);
    this.map.removeInteraction(this.draw);
  },
};
</script>
