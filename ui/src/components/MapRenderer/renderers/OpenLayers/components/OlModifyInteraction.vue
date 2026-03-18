<template>
  <div v-if="false"></div>
</template>

<script setup lang="ts">
import { inject, onUnmounted, watch } from "vue";
import type Map from "ol/Map";
import { Modify } from "ol/interaction";
import Collection from "ol/Collection";
import { useEditLayerStore } from "@/stores/edit_layer_store";
import { EditLayerMode } from "@/types/map";

const map = inject<Map | null>("map", null);

const editLayerStore = useEditLayerStore();

let modify: Modify | null = null;

const destroyModifyInteraction = () => {
  if (map && modify) {
    map.removeInteraction(modify);
    modify = null;
  }
};

const syncModifyInteraction = () => {
  if (!map) return;

  destroyModifyInteraction();

  if (editLayerStore.editLayerMode !== EditLayerMode.EDIT || !editLayerStore.highlightedFeatureAndLayer?.feature) {
    return;
  }

  const features = new Collection([editLayerStore.highlightedFeatureAndLayer.feature]);

  modify = new Modify({
    features: features,
  });

  map.addInteraction(modify);
};

watch(
  () => [editLayerStore.editLayerMode, editLayerStore.highlightedFeatureAndLayer?.feature],
  () => {
    syncModifyInteraction();
  },
  { immediate: true },
);

onUnmounted(() => {
  destroyModifyInteraction();
});
</script>
