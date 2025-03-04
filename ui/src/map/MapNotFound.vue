<template>
  <NotFound
    title="Oeps, verdwaald?"
    message="De opgevraagde URL bestaat niet (meer) of de URL is onjuist."
    link-url="/atlas/"
    link-text="Terug naar de hoofdkaart"
  />
</template>

<script setup lang="ts">
import NotFound from "@/components/NotFound.vue";
</script>

<style>
#app {
  height: 100dvh;
  width: 100dvw;
}
</style>
