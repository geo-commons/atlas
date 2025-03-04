<template>
  <NotFound
    title="Oeps, verdwaald?"
    message="De opgevraagde pagina bestaat niet (meer) of de URL is onjuist."
    link-url="/"
    link-text="Terug naar portaal"
  />
</template>

<script setup lang="ts">
import NotFound from "@/components/NotFound.vue";
</script>
