<template>
  <main class="tw-mx-auto tw-max-w-7xl tw-px-4 md:tw-pt-6 tw-my-4 tw-w-full">
    <h1 class="tw-text-4xl tw-my-0 tw-mb-2">Kaarten</h1>
    <Spinner v-if="loading" class="spinner" :style-type="'portal'" />
    <section>
      <div class="tw-w-full md:tw-w-2/6 tw-my-5">
        <PortalSearchField
          :initial-search-query="searchQuery"
          :placeholder="'Zoek op kaarten'"
          @on-search="setSearchQuery"
        />
      </div>
      <div class="tw-grid sm:tw-grid-cols-2 md:tw-grid-cols-3 lg:tw-grid-cols-4 tw-gap-4 md:tw-gap-8">
        <p class="!tw-mt-0" v-if="!maps.length > 0">Geen resultaten gevonden.</p>
        <PortalCard
          v-for="map in maps"
          :key="map.id"
          :object-type="'map'"
          :title="map.title"
          :thumbnail="map.thumbnail"
          :summary="map.description"
          :show-thumbnail="true"
          :object-url="`/atlas/maps/${map.slug}`"
        />
      </div>
      <div class="tw-flex tw-flex-row tw-items-start tw-py-8">
        <Paginator
          :first="page * items_per_page - 1"
          :rows="items_per_page"
          :total-records="total_items"
          :rows-per-page-options="[10, 20, 30]"
          :pt="{
            root: {
              class: '!tw-p-0',
            },
          }"
          @page="updatePageState"
        ></Paginator>
      </div>
    </section>
  </main>
</template>

<script>
import { useGlobalStore } from "@/stores";
import PortalCard from "@/portal/components/PortalCard.vue";
import PortalSearchField from "@/portal/components/PortalSearchField.vue";
import Spinner from "@/components/Spinner.vue";

export default {
  name: "PortalMapsPage",
  components: { PortalSearchField, PortalCard, Spinner },
  data() {
    return {
      loading: false,
      maps: [],
      searchQuery: "",
      items_per_page: 20,
      page: 1,
      total_items: 20,
    };
  },
  computed: {
    config() {
      return useGlobalStore().config;
    },
  },
  created() {
    this.getMaps();
  },
  methods: {
    async getMaps() {
      this.loading = true;

      const result = await fetch(
        `/atlas/api/v1/maps/?published=True&show_in_overview=True&search=${this.searchQuery}&page=${this.page}&page_size=${this.items_per_page}`,
        {
          credentials: "same-origin",
          headers: { "Content-Type": "application/json" },
        },
      );

      if (!result.ok) {
        console.error("Could not fetch maps");
      }

      const response = await result.json();
      this.maps = response.results;
      this.loading = false;
      this.total_items = response.count;
    },
    async setSearchQuery(newSearchQuery) {
      this.searchQuery = newSearchQuery;
      this.page = 1;
      await this.getMaps();
    },
    async updatePageState(pageState) {
      this.page = pageState.page + 1;
      this.items_per_page = pageState.rows;

      await this.getMaps();
    },
  },
};
</script>
