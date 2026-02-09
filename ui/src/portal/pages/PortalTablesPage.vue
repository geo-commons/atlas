<template>
  <PortalOverviewTemplate
    v-model:search-query="searchQuery"
    title="Tabellen"
    subtitle="Doorzoek alle beschikbare tabellen in het dataportaal. Gebruik de zoekfunctie om tabellen te vinden."
    header-icon="pi pi-chart-bar"
    search-placeholder="Zoek op tabellen..."
    :total-records="totalItems"
    :items-per-page="itemsPerPage"
    :page="page"
    :has-results="filteredTables.length > 0"
    :loading="loading"
    empty-icon="pi pi-chart-bar"
    empty-title="Geen resultaten gevonden"
    empty-message="Probeer andere zoektermen om resultaten te vinden."
    @search="handleSearch"
    @update:items-per-page="handleItemsPerPageChange"
    @page="updatePageState"
  >
    <template #filters>
      <div class="tw-grid md:tw-grid-cols-2 tw-gap-6">
        <div>
          <label class="tw-block tw-text-sm tw-font-medium tw-text-gray-700 tw-mb-2">Sorteren op</label>
          <Dropdown
            v-model="selectedSort"
            :options="sortOptions"
            option-label="label"
            option-value="value"
            class="tw-w-full"
            :pt="{ input: { class: 'tw-text-sm' }, panel: { class: 'tw-text-sm' } }"
            @change="handleSortChange"
          />
        </div>
      </div>
    </template>

    <template #default>
      <div class="tw-grid sm:tw-grid-cols-2 lg:tw-grid-cols-3 tw-gap-6 tw-mb-12">
        <PortalCard
          v-for="table in pagedTables"
          :key="table.id"
          :object-type="'table'"
          :title="table.title"
          :summary="table.description"
          :show-thumbnail="false"
          :object-url="`/tables/${table.slug}`"
        />
      </div>
    </template>
  </PortalOverviewTemplate>
</template>

<script setup lang="ts">
import PortalCard from "@/portal/components/PortalCard.vue";
import PortalOverviewTemplate from "@/portal/components/PortalOverviewTemplate.vue";
import { computed, ref } from "vue";
import type { PageState } from "primevue/paginator";
import Dropdown from "primevue/dropdown";
import { useGlobalStore } from "@/stores";

interface Table {
  id: number;
  title: string;
  description?: string;
  slug: string;
  thumbnail?: string;
}

interface SortOption {
  label: string;
  value: string;
}

const loading = ref(false);
const globalStore = useGlobalStore();
const allTables = computed<Table[]>(() => globalStore.tables || []);
const searchQuery = ref("");
const selectedSort = ref("title");
const page = ref(1);
const itemsPerPage = ref(12);

const sortOptions: SortOption[] = [
  { label: "Titel (A-Z)", value: "title" },
  { label: "Titel (Z-A)", value: "-title" },
];

const normalizedQuery = computed(() => searchQuery.value.trim().toLowerCase());
const filteredTables = computed(() => {
  if (!normalizedQuery.value) {
    return allTables.value;
  }

  return allTables.value.filter((table) => table.title?.toLowerCase().includes(normalizedQuery.value));
});

const sortedTables = computed(() => {
  const sorted = [...filteredTables.value].sort((a, b) =>
    a.title.localeCompare(b.title, "nl", { sensitivity: "base" }),
  );
  return selectedSort.value === "-title" ? sorted.reverse() : sorted;
});

const pagedTables = computed(() => {
  const start = (page.value - 1) * itemsPerPage.value;
  return sortedTables.value.slice(start, start + itemsPerPage.value);
});

const totalItems = computed(() => filteredTables.value.length);

const handleSearch = () => {
  page.value = 1;
};

const handleSortChange = () => {
  page.value = 1;
};

const handleItemsPerPageChange = (v: number) => {
  itemsPerPage.value = v;
  page.value = 1;
};

const updatePageState = (pageState: PageState) => {
  page.value = pageState.page + 1;
  itemsPerPage.value = pageState.rows;
};
</script>
