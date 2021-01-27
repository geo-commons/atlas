<template>
  <div class="wrapper">
    <button class="iconbutton" :class="{ isActive: this.tool === 'SELECT_AREA' }" @click="toggle" aria-label="Selecteer adres">
      <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M3 5h2V3c-1.1 0-2 .9-2 2zm0 8h2v-2H3v2zm4 8h2v-2H7v2zM3 9h2V7H3v2zm10-6h-2v2h2V3zm6 0v2h2c0-1.1-.9-2-2-2zM5 21v-2H3c0 1.1.9 2 2 2zm-2-4h2v-2H3v2zM9 3H7v2h2V3zm2 18h2v-2h-2v2zm8-8h2v-2h-2v2zm0 8c1.1 0 2-.9 2-2h-2v2zm0-12h2V7h-2v2zm0 8h2v-2h-2v2zm-4 4h2v-2h-2v2zm0-16h2V3h-2v2zM7 17h10V7H7v10zm2-8h6v6H9V9z" fill="currentColor" /></svg>
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
        this.$emit('set-selected-area', null)
      }
    }
  },
  props: {
    tool: String
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