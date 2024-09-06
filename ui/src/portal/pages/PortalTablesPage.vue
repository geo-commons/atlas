<template>
  <div class="container __portal">
    <h1 class="__portal">Tabellen</h1>
    <section>
      <div class="search-container">
        <PortalSearchField
          :initial-search-query="searchQuery"
          :placeholder="'Zoek op tabellen'"
          @on-search="setSearchQuery"
        />
      </div>
      <div class="tables-container">
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

<style scoped>
h2 {
  font-size: var(--font-size-3xl);
  margin: 20px 0;
}

.tables-container {
  display: flex;
  flex-wrap: wrap;
  gap: 60px;
}
</style>
