<template>
  <div v-if="false"></div>
</template>

<script>
import { DragZoom } from "ol/interaction";

export default {
  name: "OlDragZoom",
  inject: ["map"],
  props: {
    tool: String,
  },
  created() {
    this.dragZoom = new DragZoom();
    this.map.addInteraction(this.dragZoom);
  },
  destroyed() {
    this.map.removeInteraction(this.dragZoom);
  },
};
</script>
