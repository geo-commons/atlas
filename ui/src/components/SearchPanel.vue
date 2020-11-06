<template>
  <div>
    <form method="GET" @submit="onSubmit">
      <input type="text" name="search" placeholder="Zoek adres.." />
      <button type="submit">Zoek</button>
    </form>
  </div>
</template>

<script>
export default {
  name: 'SearchPanel',
  methods: {
    onSubmit(e) {
      e.preventDefault()
    }
  },
}
</script>

<style scoped>
</style>
