<template>
  <div v-if="false"></div>
</template>

<script>
import constructDraw from "../../../../../utils/draw";

export default {
  name: "OlDrawInteraction",
  inject: ["map"],
  props: {
    layers: Array,
    tool: String,
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
