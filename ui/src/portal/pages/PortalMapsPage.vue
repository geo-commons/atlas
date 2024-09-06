<template>
  <div class="container __portal">
    <h1 class="__portal">Kaarten</h1>
    <Spinner v-if="loading" class="spinner" :style-type="'portal'" />
    <section>
      <div class="search-container">
        <PortalSearchField
          :initial-search-query="searchQuery"
          :placeholder="'Zoek op kaarten'"
          @on-search="setSearchQuery"
        />
      </div>
      <div class="card-container">
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
  </div>
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

      const result = await fetch("/atlas/api/v1/maps/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch maps");
      }

      this.maps = await result.json();
      this.loading = false;
    },
    setSearchQuery(newSearchQuery) {
      this.searchQuery = newSearchQuery;
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
