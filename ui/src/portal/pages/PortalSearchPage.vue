<template>
  <div class="container __portal">
    <h1 class="__portal">Alle zoekresultaten voor: "{{ searchQuery }}" ({{ datasets.length }} resultaten)</h1>
    <Spinner v-if="loading" class="spinner" :style-type="'portal'" />
    <section v-else class="search-results-wrapper">
      <div class="search-container">
        <PortalSearchField :initial-search-query="searchQuery" @on-search="onSearch" />
      </div>
      <div v-if="results > 0">
        <div v-if="datasets.length > 0">
          <h3>Datasets</h3>
          <PortalDatasetList :datasets="datasets" />
        </div>
      </div>
      <div v-else class="no-results-wrapper">
        <p>Helaas er zijn geen resultaten gevonden voor de zoekopdracht: "{{ searchQuery }}"</p>
      </div>
    </section>
  </div>
</template>

<script>
import Spinner from "@/components/Spinner.vue";
import PortalDatasetList from "@/portal/components/dataset/PortalDatasetList.vue";
import PortalSearchField from "@/portal/components/PortalSearchField.vue";

export default {
  name: "PortalSearchPage",
  components: { PortalDatasetList, Spinner, PortalSearchField },
  data() {
    return {
      loading: false,
      datasets: [],
      searchQuery: "",
    };
  },
  computed: {
    results() {
      return this.datasets.length;
    },
  },
  created() {
    this.searchQuery = this.$route.query.query;
    this.getDatasets();
  },
  methods: {
    async getDatasets() {
      this.loading = true;

      const result = await fetch(`/atlas/api/v1/datasets/?search=${this.searchQuery}`, {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch datasets");
      }

      this.datasets = await result.json();
      this.loading = false;
    },
    onSearch(searchQuery) {
      this.searchQuery = searchQuery;
      this.getDatasets();
    },
  },
};
</script>

<style scoped>
h3 {
  margin: 0;
  font-size: var(--font-size-xl);
}

@media (min-width: 1024px) {
  h3 {
    margin: 12px 0;
    font-size: var(--font-size-2xl);
  }
}

.search-results-wrapper {
  flex: 1;
}

.no-results-wrapper {
  padding-top: 20px;
}
</style>
