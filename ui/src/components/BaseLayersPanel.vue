<template>
  <div id="baseLayers" class="wrapper">
    <ul>
      <li v-for="layer in baseLayers" :key="layer.id" class="layer">
        <input
          :id="layer.id"
          type="radio"
          name="baseLayer"
          :checked="layer.is_visible"
          @click="() => onSelect(layer)"
        />
        <label :for="layer.id">{{ layer.title }}</label>
        <LayerInfo :layer="layer" />
      </li>
      <li class="layer">
        <input
          id="baseLayer_null"
          type="radio"
          name="baseLayer"
          :checked="noSelectedBaseLayer"
          @click="() => onSelect(null)"
        />
        <label for="baseLayer_null">Geen</label>
      </li>
    </ul>
  </div>
</template>

<script>
import LayerInfo from "./LayerInfo";
import { useMapStore } from "@/stores/map_store";

export default {
  name: "BaseLayersPanel",
  components: {
    LayerInfo,
  },
  props: {
    mapId: String,
  },
  data() {
    return {
      mapStore: null,
    };
  },
  computed: {
    baseLayers() {
      return this.mapStore ? this.mapStore.baseLayers : [];
    },
    noSelectedBaseLayer() {
      return this.mapStore ? this.mapStore.selectedBaseLayer === null : true;
    },
  },
  mounted() {
    this.mapStore = useMapStore(this.mapId);
  },
  methods: {
    onSelect(selectedLayer) {
      if (!selectedLayer) {
        this.mapStore.deselectBaseLayer();
        return;
      }

      if (selectedLayer.is_visible) {
        return;
      }

      this.mapStore.toggleBaseLayer({ selectedLayerId: selectedLayer.id, is_visible: !selectedLayer.is_visible });
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
