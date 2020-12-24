<template>
  <div class="wrapper">
    <button class="iconbutton" :class="{ isActive: this.tool === 'SELECT_AREA' }" @click="toggle" aria-label="Selecteer adres">
      <svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24" viewBox="0 0 24 24" width="24"><g><rect fill="none" height="24" width="24"/><path fill="currentColor" d="M17,5h-2V3h2V5z M15,15v6l2.29-2.29L19.59,21L21,19.59l-2.29-2.29L21,15H15z M19,9h2V7h-2V9z M19,13h2v-2h-2V13z M11,21h2 v-2h-2V21z M7,5h2V3H7V5z M3,17h2v-2H3V17z M5,21v-2H3C3,20.1,3.9,21,5,21z M19,3v2h2C21,3.9,20.1,3,19,3z M11,5h2V3h-2V5z M3,9h2 V7H3V9z M7,21h2v-2H7V21z M3,13h2v-2H3V13z M3,5h2V3C3.9,3,3,3.9,3,5z" /></g></svg>
    </button>
  </div>
</template>

<script>
export default {
  name: 'AreaSelectPanel',
  methods: {
    toggle() {
      if (this.tool !== 'SELECT_AREA') {
        this.$emit('set-tool', 'SELECT_AREA')
      } else {
        // toggle off when the user is currently selecting an area
        this.$emit('set-tool', '')
      }
    }
  },
  computed: {
    visibleLayers() {
      return this.layers.filter((layer) => !layer.is_base && layer.is_visible)
    }
  },
  props: {
    tool: String,
    layers: Array
  }
}
</script>

<style scoped>
.wrapper {
  display: flex;
  margin-right: 12px;
  background: white;
  border-radius: var(--radius-small);
  overflow: hidden;
  box-shadow: var(--shadow-normal);
}

.iconbutton {
  width: var(--width-button-large);
  height: var(--width-button-large);
}

.iconbutton.isActive {
  color: var(--color-primary);
}

.menu {
  position: absolute;
  top: var(--width-button-large);
  right: 0;
  padding: 4px 0;
  background: white;
  border-radius: var(--radius-small);
  border-top-right-radius: 0;
  box-shadow: var(--shadow-normal);
  transform: translateY(0);
}

.list a {
  display: block;
  color: black;
  text-decoration: none;
  padding: 2px 12px;
  font-size: var(--font-size-small);
}

.list a:hover {
  background: #F5F5F5;
}

.list a:active {
  background: #EAEAEA;
}
</style>
