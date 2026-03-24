<template>
  <div v-if="false"></div>
</template>

<script setup lang="ts">
import { inject, onUnmounted, watch } from "vue";
import type Map from "ol/Map";
import { Modify, Snap } from "ol/interaction";
import Collection from "ol/Collection";
import { useEditLayerStore } from "@/stores/edit_layer_store";
import { EditLayerMode } from "@/types/map";
import { Feature } from "ol";
import { Geometry } from "ol/geom";

const map = inject<Map | null>("map", null);

const editLayerStore = useEditLayerStore();

let modify: Modify | null = null;
let snap: Snap | null = null;

const destroyModifyInteraction = () => {
  if (map && snap) {
    map.removeInteraction(snap);
    snap = null;
  }

  if (map && modify) {
    map.removeInteraction(modify);
    modify = null;
  }
};

const syncModifyInteraction = () => {
  if (!map) return;

  destroyModifyInteraction();

  if (
    editLayerStore.editLayerMode !== EditLayerMode.EDIT ||
    editLayerStore.isRedrawingFeature ||
    !editLayerStore.highlightedFeatureAndLayer?.feature
  ) {
    return;
  }

  const feature = editLayerStore.highlightedFeatureAndLayer.feature as Feature<Geometry>;
  const features = new Collection([feature]);

  modify = new Modify({
    features: features,
    // hides the handles of the modify interaction, because they are not needed
    style: () => undefined,
  });

  modify.on("modifyend", (event) => {
    const modifiedFeature = event.features.getArray()[0];
    editLayerStore.setModifiedFeature(modifiedFeature);
  });

  map.addInteraction(modify);

  snap = new Snap({
    features: features,
    edge: true,
    vertex: true,
  });

  map.addInteraction(snap);
};

watch(
  () => [
    editLayerStore.editLayerMode,
    editLayerStore.highlightedFeatureAndLayer?.feature,
    editLayerStore.isRedrawingFeature,
  ],
  () => {
    syncModifyInteraction();
  },
  { immediate: true },
);

onUnmounted(() => {
  destroyModifyInteraction();
});
</script>
