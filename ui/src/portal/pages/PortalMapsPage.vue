<template>
  <main class="tw-mx-auto tw-max-w-7xl tw-px-4 md:tw-pt-6 tw-my-4 tw-w-full">
    <h1 class="tw-text-4xl tw-my-0 tw-mb-2">Kaarten</h1>
    <Spinner v-if="loading" class="spinner" :style-type="'portal'" />
    <section class="">
      <div class="tw-w-full md:tw-w-2/6 tw-my-5">
        <PortalSearchField
          :initial-search-query="searchQuery"
          :placeholder="'Zoek op kaarten'"
          @on-search="setSearchQuery"
        />
      </div>
      <div class="tw-grid sm:tw-grid-cols-2 md:tw-grid-cols-3 lg:tw-grid-cols-4 tw-gap-4 md:tw-gap-8">
        <PortalCard
          v-for="map in visibleMaps"
          :key="map.id"
          :object-type="'map'"
          :title="map.title"
          :thumbnail="map.thumbnail"
          :summary="map.description"
          :show-thumbnail="true"
          :object-url="`/atlas/maps/${map.slug}`"
        />
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
    };
  },
  computed: {
    config() {
      return useGlobalStore().config;
    },
    visibleMaps() {
      if (!this.searchQuery) {
        return this.maps;
      }

      // todo: check if this is the way we want to perform a search
      return Object.values(this.maps).filter(
        (map) => map.title.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1,
      );
    },
  },
  created() {
    this.getMaps();
  },
  methods: {
    async getMaps() {
      this.loading = true;

      const result = await fetch("/atlas/api/v1/maps/?published=True&show_in_overview=True", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch maps");
      }

      const response = await result.json();
      this.maps = response.results;
      this.loading = false;
    },
    setSearchQuery(newSearchQuery) {
      this.searchQuery = newSearchQuery;
    },
  },
};
</script>
