<template>
  <div class="select-menu tools-panel__button-container">
    <button
      v-tippy="{ placement: 'bottom' }"
      class="tools-panel__button"
      :class="{
        'tools-panel__button--active': tool === 'SELECT_AREA' || tool === 'SELECT_CIRCLE' || tool === 'SELECT_FEATURE',
      }"
      content="Selecteer gebied"
      aria-label="Selecteer gebied"
      @click="toggleSelectArea"
    >
      <AreaSelectIcon class="icon __smedium" />
    </button>

    <div v-if="showSelectMenu" class="tools-panel__menu">
      <transition name="fade">
        <ul class="tools-panel__list">
          <li>
            <button aria-label="Selecteer gebied met behulp van cirkel" @click="() => setTool('SELECT_CIRCLE')">
              Cirkel
            </button>
          </li>
          <li>
            <button aria-label="Selecteer gebied met behulp van polygoon" @click="() => setTool('SELECT_AREA')">
              Polygoon
            </button>
          </li>
        </ul>
      </transition>
    </div>
  </div>
</template>

<script setup lang="ts">
import AreaSelectIcon from "@/assets/icons/area-select-icon.svg";

interface SelectMenuProps {
  showSelectMenu: boolean;
  setTool: (tool: string) => void;
  tool: string;
  toggleSelectArea: () => void;
}

const { showSelectMenu, setTool, tool, toggleSelectArea } = defineProps<SelectMenuProps>();
</script>
