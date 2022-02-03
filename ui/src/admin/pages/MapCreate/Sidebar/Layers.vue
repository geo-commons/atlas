<template>
    <div class="content">
        <button @click="() => this.$emit('show-form')">Terug</button>
    </div>
</template>

<script>
export default {
    name: 'Layers',
}
</script>

<style scoped>
.content {
    width: 100%;
}
</style>
