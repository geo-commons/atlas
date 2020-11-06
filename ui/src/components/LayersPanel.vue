<template>
  <div>
    <button @click="toggle">Layers</button>
    <div v-if="isOpen">
      <ul>
        <li v-for="layer in layers" :key="layer.id">
          {{ layer.id }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LayersPanel',
  data() {
    return {
      isOpen: false
    }
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen
    }
  },
  props: {
    layers: Array,
  }
}
</script>

<style scoped>
</style>
