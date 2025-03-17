<template>
  <NotFound
    title="Oeps, verdwaald?"
    message="De opgevraagde pagina bestaat niet (meer) of de URL is onjuist."
    link-url="/atlas/admin/"
    link-text="Terug naar de beheerpagina"
  />
</template>

<script setup lang="ts">
import NotFound from "@/components/NotFound.vue";
</script>
