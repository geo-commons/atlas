<template>
  <div class="measure-menu tools-panel__button-container">
    <button
      v-tippy="{ placement: 'bottom' }"
      class="tools-panel__button"
      :class="{
        'tools-panel__button--active': tool === 'MEASURE_AREA' || tool === 'MEASURE_LINE',
      }"
      content="Opmeten"
      aria-label="Opmeten"
      @click="toggleMeasure"
    >
      <RulerIcon class="icon" />
    </button>

    <div v-if="showMeasureMenu" class="tools-panel__menu">
      <transition name="fade">
        <ul class="tools-panel__list">
          <li>
            <button aria-label="Meet oppervlakte" @click="() => setTool('MEASURE_AREA')">Oppervlakte</button>
          </li>
          <li>
            <button aria-label="Meet afstand" @click="() => setTool('MEASURE_LINE')">Afstand</button>
          </li>
        </ul>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import RulerIcon from "@/assets/icons/ruler-icon.svg";

interface MeasureMenuProps {
  showMeasureMenu: boolean;
  setTool: (tool: string) => void;
  tool: string;
  toggleMeasure: () => void;
}

const { showMeasureMenu, setTool, tool, toggleMeasure } = defineProps<MeasureMenuProps>();
</script>
