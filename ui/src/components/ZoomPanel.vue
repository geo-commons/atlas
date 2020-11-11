<template>
  <div class="wrapper">
    <button class="iconbutton" @click="zoomIn" aria-label="Zoom in"><svg width="10px" height="10px" viewBox="0 0 10 10" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g id="Symbols" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><polygon id="Path" fill="#000000" points="4 10 6 10 6 6 10 6 10 4 6 4 6 0 4 0 4 4 0 4 0 6 4 6"></polygon></g></svg></button>
    <button class="iconbutton" @click="zoomOut" aria-label="Zoom uit"><svg width="10px" height="2px" viewBox="0 0 10 2" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"><g id="Symbols" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"><polygon id="Path" fill="#000000" points="10 2 10 0 0 0 0 2"></polygon></g></svg></button>
  </div>
</template>

<script>
export default {
  name: 'ZoomPanel',
  methods: {
    zoomIn() {
      this.$emit('set-position', { ...this.position, zoom: (this.position.zoom + 1) })
    },
    zoomOut() {
      this.$emit('set-position', { ...this.position, zoom: (this.position.zoom - 1) })
    }
  },
  props: {
    position: Object,
  }
}
</script>

<style scoped>
.wrapper {
  position: fixed;
  bottom: 16px;
  right: 16px;
  display: flex;
  flex-direction: column;
  background: white;
  border-radius: 6px;
  overflow: hidden;
  box-shadow: 0 0 4px rgba(0,0,0,.1), 0 0 12px rgba(0,0,0,.15);
}

.iconbutton {
  width: 32px;
  height: 32px;
}

.iconbutton:not(:last-child) {
  border-bottom: 1px solid #EAEAEA;
}

</style>
