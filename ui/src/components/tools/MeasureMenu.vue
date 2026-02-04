<template>
  <div class="measure-menu tools-panel__button-container">
    <button
      v-tippy="{ placement: 'bottom' }"
      class="tools-panel__button"
      :class="{
        'tools-panel__button--active': showMeasureMenu || tool === 'MEASURE_AREA' || tool === 'MEASURE_LINE',
      }"
      content="Opmeten"
      aria-label="Opmeten"
      @click="toggleMeasure"
    >
      <RulerIcon class="icon" />
    </button>

    <div>
      <transition name="fade">
        <div v-if="showMeasureMenu || tool === 'MEASURE_AREA' || tool === 'MEASURE_LINE'" class="tools-panel__draw-bar">
          <div class="tools-panel__draw-menu">
            <button
              v-tippy="{ placement: 'bottom' }"
              aria-label="Meet afstand (lijn)"
              class="tools-panel__button"
              :class="{ 'tools-panel__button--active': tool === 'MEASURE_LINE' }"
              content="Afstand"
              @click="() => setTool('MEASURE_LINE')"
            >
              <LineIcon />
            </button>
          </div>
          <div class="tools-panel__draw-menu">
            <button
              v-tippy="{ placement: 'bottom' }"
              aria-label="Meet oppervlakte (polygoon)"
              class="tools-panel__button"
              :class="{ 'tools-panel__button--active': tool === 'MEASURE_AREA' }"
              content="Oppervlakte"
              @click="() => setTool('MEASURE_AREA')"
            >
              <PolyGonIcon />
            </button>
          </div>
          <button
            v-tippy="{ placement: 'bottom' }"
            aria-label="Verwijder meting"
            class="tools-panel__button tools-panel__button--delete"
            content="Verwijder meting"
            :disabled="!hasMeasuredAreas"
            @click="clearMeasuredAreas"
          >
            <DeleteIcon />
          </button>
        </div>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import DeleteIcon from "@/assets/icons/delete-icon.svg";
import LineIcon from "@/assets/icons/line-icon.svg";
import PolyGonIcon from "@/assets/icons/polygon-icon.svg";
import RulerIcon from "@/assets/icons/ruler-icon.svg";
import { useMapStore } from "@/stores/map_store";
import { computed } from "vue";

interface MeasureMenuProps {
  showMeasureMenu: boolean;
  setTool: (tool: string) => void;
  tool: string;
  toggleMeasure: () => void;
  mapRef?: any;
  mapId?: string;
}

const { showMeasureMenu, setTool, tool, toggleMeasure, mapRef, mapId } = defineProps<MeasureMenuProps>();
const mapStore = useMapStore(mapId || "primary");

const hasMeasuredAreas = computed(() => mapStore.measuredAreas.length > 0);

const clearMeasuredAreas = () => {
  if (hasMeasuredAreas.value) {
    mapStore.clearMeasuredAreas();
    // Remove all tooltips of measured areas from the map
    if (mapRef && mapRef.clearMeasuredAreaTooltips) {
      mapRef.clearMeasuredAreaTooltips();
    }
    setTool("");
  }
};
</script>
