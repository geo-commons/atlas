<template>
  <Message
    severity="warn"
    :pt="{
      root: 'tw-px-5 md:tw-px-8 tw-py-1',
      content: '!tw-px-0 !tw-rounded-none',
    }"
  >
    U bevindt zich op een verouderde themakaart. Via
    <a class="link" :href="`/atlas/maps/${themeSlug}`">deze url</a> kunt u de nieuwe themakaart bezoeken.
  </Message>
</template>

<script setup lang="ts">
interface OutdatedMapAlertProps {
  themeSlug: string;
}

const { themeSlug } = defineProps<OutdatedMapAlertProps>();
</script>

<style scoped>
.link {
  color: var(--prime-yellow-700);
}
</style>
