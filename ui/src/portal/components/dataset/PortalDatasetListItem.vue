<template>
  <router-link
    :to="{ name: 'dataset-details', params: { slug: dataset.slug } }"
    class="card-link"
    type="button"
    aria-label="Naar details dataset"
  >
    <h2>{{ dataset.title }}</h2>
    <div class="sub-text">Laatst bijgewerkt: {{ formatDateValue(dataset.last_updated) }}</div>
    <div class="sub-text">Gegevensbeheerder: {{ dataset.data_owner }}</div>
    <p>{{ dataset.description }}</p>
    <ul class="theme-list">
      <li v-for="theme in dataset.themes" :key="theme.id">
        <PortalThemeCard :theme="theme" />
      </li>
    </ul>
  </router-link>
</template>

<script>
import { formatDateValue } from "@/utils/date-formatter";
import PortalThemeCard from "@/portal/components/PortalThemeCard.vue";

export default {
  name: "PortalDatasetListItem",
  components: { PortalThemeCard },
  props: { dataset: Object },
  methods: { formatDateValue },
};
</script>

<style scoped>
h2 {
  margin-bottom: 0;
  font-size: var(--font-size-large);
  color: var(--color-primary-organization);
}

@media (min-width: 1024px) {
  h2 {
    font-size: var(--font-size-xl);
    margin: 0;
  }
}
.sub-text {
  color: var(--color-text-grey);
  font-size: var(--font-size-small);
}

.card-link {
  text-decoration: none;
  color: var(--color-black);
  padding: 0;
  max-width: 250px;
}

.card-link:hover {
  cursor: pointer;
}

.card-link:focus {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

.card-link:hover > h2 {
  text-decoration: underline;
}

.theme-list {
  list-style-type: none;
  display: flex;
  gap: 8px;
  padding-bottom: 16px;
}

.theme-list > li {
  float: left;
}
</style>
