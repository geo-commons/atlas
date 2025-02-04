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

<style scoped>
.menu {
  position: absolute;
  top: var(--width-button-large);
  padding: 6px 0;
  background: white;
  border-radius: var(--radius-small);
  border-top-right-radius: 0;
  box-shadow: var(--shadow-normal);
}

.list a,
.list button {
  display: block;
  width: 100%;
  color: black;
  text-decoration: none;
  padding: 4px 12px;
  font-size: var(--font-size-small);
}

.list a:hover,
.list button:hover {
  background: var(--color-grey-40);
}

.list a:active,
.list button:active {
  background: var(--color-grey-50);
}
</style>
