<template>
  <div>
    <button @click="toggle">Meer...</button>
    <div v-if="this.isOpen">
      <ul>
        <li><a href="#">Log in</a></li>
        <li><a href="#">Help</a></li>
        <li><a href="#">Print</a></li>
        <li><a href="#">Deel</a></li>
        <li><a href="#">Embed</a></li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'MorePanel',
  data() {
    return {
      isOpen: false
    }
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen
    }
  }
}
</script>

<style scoped>
</style>
