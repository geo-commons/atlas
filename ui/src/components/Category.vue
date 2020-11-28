<template>
  <li>
    <button @click="toggle" :aria-expanded="isOpen.toString()" :aria-controls="category.id">{{ isOpen ? "-" : "+" }} {{ category.title }}</button>
    <ul :id="category.id" v-if="isOpen" class="layers">
      <slot />
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
