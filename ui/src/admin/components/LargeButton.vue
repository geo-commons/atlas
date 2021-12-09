<template>
    <div class="large-button">
        <slot />
    </div>
</template>

<script>
export default {
    name: 'LargeButton',
}
</script>

<style scoped>
.large-button {
    border: 1px solid var(--color-grey-60);
    border-radius: var(--radius-normal);
    padding: 14px;
    text-align: center;
}

a .large-button {
    color: #000;
    font-size: var(--font-size-medium);
}
</style>
