<template>
  <div
    v-if="showCompareLayerPanel"
    class="tw-flex tw-items-center tw-bg-white tw-h-12 tw-px-4 tw-rounded-sm tw-shadow-md"
  >
    <Slider
      :model-value="mapStore.comparePercentage"
      class="tw-w-full sm:tw-w-60"
      @update:model-value="(v) => mapStore.setComparePercentage(v)"
    />
  </div>
</template>

<script setup lang="ts">
import { useMapStore } from "@/stores/map_store";

interface CompareLayersSliderProps {
  mapId: string;
  showCompareLayerPanel: boolean;
}

// Props
const { mapId, showCompareLayerPanel } = defineProps<CompareLayersSliderProps>();

// Store
const mapStore = useMapStore(mapId);
</script>
