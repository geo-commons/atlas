<template>
  <div class="tw-mx-auto tw-max-w-7xl tw-px-4 md:tw-pt-6 tw-my-4 tw-w-full">
    <h1 class="tw-text-2xl md:tw-text-4xl tw-my-0 tw-mb-2">
      Alle zoekresultaten voor: "{{ searchQuery }}" ({{ datasets.length }} resultaten)
    </h1>
    <Spinner v-if="loading" class="spinner" :style-type="'portal'" />
    <section v-else class="tw-flex-1">
      <div class="tw-w-full md:tw-w-2/6 tw-my-5">
        <PortalSearchField :initial-search-query="searchQuery" @on-search="onSearch" />
      </div>
      <div v-if="results > 0">
        <div v-if="datasets.length > 0">
          <h3 class="tw-m-0 tw-text-3xl md:tw-mt-6 md:tw-mb-2">Metadatasets</h3>
          <PortalDatasetList :datasets="datasets" />
        </div>
      </div>
      <div v-else class="tw-mt-4">
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

      const response = await result.json();
      this.datasets = response.results;
      this.loading = false;
    },
    onSearch(searchQuery) {
      this.searchQuery = searchQuery;
      this.getDatasets();
    },
  },
};
</script>
