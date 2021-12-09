<template>
    <div class="container">
        <slot />
    </div>
</template>

<script>
export default {
    name: 'Content',
}
</script>

<style scoped>
.container {
    padding: 14px 32px;
}
</style>
