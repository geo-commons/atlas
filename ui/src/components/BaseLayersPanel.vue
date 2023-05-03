<template>
  <div id="baseLayers" class="wrapper">
    <ul>
      <li v-for="layer in baseLayers" :key="layer.id" class="layer">
        <input
          :id="layer.id"
          type="radio"
          name="baseLayer"
          :checked="layer.is_visible"
          @change="() => onSelect(layer)"
        />
        <label :for="layer.id">{{ layer.title }}</label>
        <LayerInfo :layer="layer" />
      </li>
      <li class="layer">
        <input
          id="baseLayer_null"
          type="radio"
          name="baseLayer"
          :checked="allBaseLayersUnvisible"
          @change="() => onSelect(null)"
        />
        <label for="baseLayer_null">Geen</label>
      </li>
    </ul>
  </div>
</template>

<script>
import LayerInfo from "./LayerInfo";

export default {
  name: "BaseLayersPanel",
  components: {
    LayerInfo,
  },
  props: {
    layers: Array,
  },
  computed: {
    baseLayers() {
      return this.layers.filter((layer) => layer.is_base);
    },
    allBaseLayersUnvisible() {
      return this.baseLayers.every((layer) => !layer.is_visible);
    },
  },
  methods: {
    onSelect(selectedLayer) {
      this.baseLayers.map((layer) => {
        if (selectedLayer && selectedLayer.id === layer.id) {
          this.$emit("toggle-layer", [layer.id, true]);
        } else {
          this.$emit("toggle-layer", [layer.id, false]);
        }
      });
    },
  },
};
</script>

<style scoped>
.wrapper {
  position: absolute;
  bottom: 100%;
  right: 0;
  padding: 8px 12px;
  background: white;
  border-radius: var(--radius-small);
  border-bottom-right-radius: 0;
  box-shadow: var(--shadow-normal);
}

.layer {
  position: relative;
  display: flex;
}

.layer > input {
  position: absolute;
  top: 6px;
  left: 0;
  width: 12px;
  height: 12px;
  margin: 0;
}

.layer > label {
  display: block;
  position: relative;
  width: 100%;
  cursor: pointer;
  padding: 3px 0 3px 18px;
  user-select: none;
  font-size: var(--font-size-small);
  white-space: nowrap;
}
</style>
