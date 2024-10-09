<template>
  <div class="tw-mx-auto tw-max-w-7xl tw-px-4 md:tw-pt-6 tw-my-4 tw-w-full">
    <h1 class="tw-text-4xl tw-my-0 tw-mb-2">Tabellen</h1>
    <section>
      <div class="tw-w-full md:tw-w-2/6 tw-my-5">
        <PortalSearchField
          :initial-search-query="searchQuery"
          :placeholder="'Zoek op tabellen'"
          @on-search="setSearchQuery"
        />
      </div>
      <div class="tw-grid sm:tw-grid-cols-2 md:tw-grid-cols-3 lg:tw-grid-cols-4 tw-gap-4 md:tw-gap-8">
        <PortalCard
          v-for="table in visibleTables"
          :key="table.id"
          :object-type="'table'"
          :title="table.title"
          :summary="table.description"
          :thumbnail="table.thumbnail"
          :show-thumbnail="true"
          :object-url="`/tables/#/${table.slug}`"
        />
      </div>
    </section>
  </div>
</template>

<script>
import { useGlobalStore } from "@/stores";
import PortalCard from "@/portal/components/PortalCard.vue";
import PortalSearchField from "@/portal/components/PortalSearchField.vue";

export default {
  name: "PortalTablesPage",
  components: { PortalSearchField, PortalCard },
  data() {
    return {
      searchQuery: "",
    };
  },
  computed: {
    config() {
      return useGlobalStore().config;
    },
    tables() {
      return useGlobalStore().tables;
    },
    visibleTables() {
      if (!this.searchQuery) {
        return this.tables;
      }

      // todo: check if this is the way we want to perform a search
      return Object.values(this.tables).filter(
        (table) => table.title.toLowerCase().search(this.searchQuery.toLowerCase()) !== -1,
      );
    },
  },
  created() {},
  methods: {
    setSearchQuery(newSearchQuery) {
      this.searchQuery = newSearchQuery;
    },
  },
};
</script>
