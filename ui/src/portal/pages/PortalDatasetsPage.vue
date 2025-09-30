<template>
  <div class="container __portal">
    <h1 class="__portal">Metadatasets</h1>
    <Spinner v-if="loading" class="spinner" :style-type="'portal'" />
    <section v-else>
      <div class="search-container">
        <PortalSearchField :initial-search-query="searchQuery" @on-search="setSearchQuery" />
      </div>
      <PortalDatasetList :datasets="datasets" />
    </section>
  </div>
</template>

<script>
import PortalSearchField from "@/portal/components/PortalSearchField.vue";
import Spinner from "@/components/Spinner.vue";
import PortalDatasetList from "@/portal/components/dataset/PortalDatasetList.vue";

export default {
  name: "PortalDatasetPage",
  components: { PortalDatasetList, PortalSearchField, Spinner },
  data() {
    return {
      loading: false,
      datasets: [],
      searchQuery: "",
    };
  },
  created() {
    this.getDatasets();
  },
  methods: {
    async getDatasets() {
      this.loading = true;

      let fetchUrl = "/atlas/api/v1/datasets/?published=True&show_in_overview=True";

      if (this.searchQuery) {
        fetchUrl += `?search=${this.searchQuery}`;
      }

      const result = await fetch(fetchUrl, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch datasets");
      }
      const response = await result.json();
      this.datasets = response.results;
      this.loading = false;
    },
    setSearchQuery(newSearchQuery) {
      this.searchQuery = newSearchQuery;
      this.getDatasets();
    },
  },
};
</script>

<style scoped>
h2 {
  font-size: var(--font-size-3xl);
  margin: 20px 0;
}
</style>
