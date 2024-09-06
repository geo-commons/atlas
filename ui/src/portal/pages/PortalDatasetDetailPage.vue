<template>
  <div class="container __portal">
    <Spinner v-if="loading" class="spinner" :style-type="'portal'" />
    <div v-else-if="error">Er is iets fout gegaan bij het ophalen van de data...</div>
    <div v-else>
      <h1 class="__portal">{{ dataset.title }}</h1>

      <section class="dataset-details-wrapper">
        <div>
          <h3>Omschrijving</h3>
          <p>{{ dataset.description }}</p>
        </div>

        <div class="details-wrapper">
          <div>
            <h3>Details dataset</h3>
            <table class="dataset-detail-table">
              <tbody>
                <tr v-if="dataset.source_description">
                  <td>Bron omschrijving</td>
                  <td>
                    {{ dataset.source_description }}
                  </td>
                </tr>
                <tr v-if="dataset.organization">
                  <td>Organisatie</td>
                  <td>
                    {{ dataset.organization }}
                  </td>
                </tr>
                <tr v-if="dataset.contact">
                  <td>Contactpersoon</td>
                  <td>
                    {{ dataset.contact }}
                  </td>
                </tr>
                <tr v-if="dataset.data_owner">
                  <td>Eigenaar van de data</td>
                  <td>
                    {{ dataset.data_owner }}
                  </td>
                </tr>
                <tr v-if="dataset.data_controller">
                  <td>Data beheerder</td>
                  <td>
                    {{ dataset.data_controller }}
                  </td>
                </tr>
                <tr v-if="dataset.category">
                  <td>Categorie</td>
                  <td>
                    {{ dataset.category }}
                  </td>
                </tr>
                <tr v-if="dataset.last_updated">
                  <td>Laatste update</td>
                  <td>
                    {{ formatDateValue(dataset.last_updated) }}
                  </td>
                </tr>
                <tr v-if="dataset.update_frequency">
                  <td>Update hoeveelheid</td>
                  <td>
                    {{ dataset.update_frequency }}
                  </td>
                </tr>
                <tr v-if="dataset.purpose_of_manufacture">
                  <td>Doel van de vervaardiging</td>
                  <td>
                    {{ dataset.purpose_of_manufacture }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>

        <div v-if="dataset.themes.length > 0">
          <h3>Thema's</h3>
          <ul class="theme-list">
            <li v-for="theme in dataset.themes" :key="theme.id">
              <PortalThemeCard :theme="theme" />
            </li>
          </ul>
        </div>
      </section>
    </div>
  </div>
</template>

<script>
import Spinner from "@/components/Spinner.vue";
import { formatDateValue } from "@/utils/date-formatter";
import PortalThemeCard from "@/portal/components/PortalThemeCard.vue";

export default {
  name: "PortalDatasetDetailPage",
  components: { PortalThemeCard, Spinner },
  props: {},
  data() {
    return {
      searchQuery: "",
      loading: false,
      dataset: Object,
      error: false,
    };
  },
  created() {
    this.getDataset();
  },
  methods: {
    formatDateValue,
    async getDataset() {
      this.loading = true;

      const slug = this.$route.params.slug;

      if (!slug) {
        console.error("No valid slug");
        this.error = true;
        this.loading = false;
        return;
      }

      const result = await fetch(`/atlas/api/v1/datasets/${slug}/`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch datasets");
      }

      this.dataset = await result.json();
      this.loading = false;
    },
  },
};
</script>

<style scoped>
h3,
p {
  margin: 0;
}

.dataset-details-wrapper {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

@media (min-width: 1024px) {
  .dataset-details-wrapper {
    gap: 32px;
  }
}

.details-wrapper {
  display: grid;
  grid-template-columns: 1fr;
}

@media (min-width: 1024px) {
  .details-wrapper {
    display: grid;
    grid-template-columns: 7fr 5fr;
    column-gap: 40px;
  }
}

.dataset-detail-table {
  border-collapse: collapse;
}

.dataset-detail-table > tbody > tr > td {
  padding: 12px 4px;
}

.dataset-detail-table > tbody > tr:not(:last-child) > td {
  border-bottom: 1px solid var(--color-grey-60);
}

.dataset-detail-table > tbody > tr > td:first-child {
  color: var(--color-text-grey);
  padding-right: 12px;
}

@media (min-width: 1024px) {
  .dataset-detail-table > tbody > tr > td:first-child {
    color: var(--color-text-grey);
    padding-right: 30px;
  }
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
