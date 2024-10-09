<template>
  <div>
    <h3>Direct naar</h3>
    <ul class="navigation-list">
      <li>
        <a href="/atlas/" target="_blank" class="text-button">
          <ChevronRightIcon class="icon __large" />
          Hoofdkaart</a
        >
      </li>
      <li>
        <a href="/maps" class="text-button">
          <ChevronRightIcon class="icon __large" />
          Alle kaarten</a
        >
      </li>
      <li>
        <a href="/datasets" class="text-button">
          <ChevronRightIcon class="icon __large" />
          Alle datasets</a
        >
      </li>
      <li>
        <a href="/tables" class="text-button">
          <ChevronRightIcon class="icon __large" />
          Alle tabellen</a
        >
      </li>
    </ul>
  </div>
</template>

<script>
import ChevronRightIcon from "@/assets/icons/chevron-right-icon.svg";

export default {
  name: "PortalQuickNavigationMenu",
  components: { ChevronRightIcon },
};
</script>

<style scoped>
h3 {
  font-size: var(--font-size-2xl);
  margin: 8px 0 0;
}

@media (min-width: 1024px) {
  h3 {
    margin: 0 0 12px;
  }
}

.navigation-list {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

@media (min-width: 1024px) {
  .navigation-list {
    gap: 16px;
  }
}

.navigation-list > li {
  width: fit-content;
}

.text-button {
  font-size: var(--font-size-xl);
  color: var(--color-primary-organization);
}
</style>
