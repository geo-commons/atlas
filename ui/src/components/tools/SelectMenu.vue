<template>
  <div v-if="showSelectMenu" class="menu">
    <transition name="fade">
      <ul class="list">
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
</template>

<script setup lang="ts">
interface SelectMenuProps {
  showSelectMenu: boolean;
  setTool: (tool: string) => void;
}

const { showSelectMenu, setTool } = defineProps<SelectMenuProps>();
</script>
