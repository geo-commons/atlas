<template>
  <div v-if="showMeasureMenu" class="menu">
    <transition name="fade">
      <ul class="list">
        <li>
          <button aria-label="Meet oppervlakte" @click="() => setTool('MEASURE_AREA')">Oppervlakte</button>
        </li>
        <li>
          <button aria-label="Meet afstand" @click="() => setTool('MEASURE_LINE')">Afstand</button>
        </li>
      </ul>
    </transition>
  </div>
</template>

<script setup lang="ts">
interface MeasureMenuProps {
  showMeasureMenu: boolean;
  setTool: (tool: string) => void;
}

const { showMeasureMenu, setTool } = defineProps<MeasureMenuProps>();
</script>
