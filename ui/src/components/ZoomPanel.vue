<template>
  <div>
    <button @click="zoomIn">+</button>
    <button @click="zoomOut">-</button>
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
</style>
