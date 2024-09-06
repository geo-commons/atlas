<template>
  <!--todo: wrappen in een <a> en dan onClick zoek resultaten met zelfde thema? -->
  <div class="theme-wrapper">{{ theme.title }}</div>
</template>

<script>
export default {
  name: "PortalThemeCard",
  props: { theme: Object },
};
</script>

<style scoped>
.theme-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  padding: 4px 6px;
  background: var(--color-grey-60);
  font-size: var(--font-size-small);
}
</style>
