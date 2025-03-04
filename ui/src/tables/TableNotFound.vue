<template>
  <NotFound
    title="Oeps, verdwaald?"
    message="De opgevraagde pagina bestaat niet (meer) of de URL is onjuist."
    link-url="/tables/"
    link-text="Terug naar tabellen"
  />
</template>

<script setup lang="ts">
import NotFound from "@/components/NotFound.vue";
</script>
