<template>
  <li>
    <button @click="toggle" :aria-expanded="isOpen.toString()" :aria-controls="category.id">{{ isOpen ? "-" : "+" }} {{ category.title }}</button>
    <ul :id="category.id" v-if="isOpen" class="layers">
      <li v-for="layer in category.layers" v-bind:key="layer.id">
        <input type="checkbox" :name="layer.id" :id="layer.id" :checked="layer.is_visible" @change="() => onSelect(layer)" />
        <label :for="layer.id">{{ layer.title }}</label>
      </li>
    </ul>
  </li>
</template>

<script>
export default {
  name: 'Category',
  data() {
    return {
      isOpen: false
    }
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen
    },
    onSelect(selectedLayer) {
      this.$emit('toggle-layer', [ selectedLayer.id, !selectedLayer.is_visible ])
    }
  },
  props: {
    category: Object,
  }
}
</script>

<style scoped>
.layers {
  margin-left: 25px;
}
</style>
