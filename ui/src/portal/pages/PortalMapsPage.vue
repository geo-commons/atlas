<template>
  <PortalOverviewTemplate
    v-model:search-query="searchQuery"
    title="Kaarten"
    subtitle="Doorzoek alle beschikbare themakaarten in het dataportaal. Gebruik de zoekfunctie om kaarten te vinden."
    header-icon="pi pi-map"
    search-placeholder="Zoek op kaarten..."
    :total-records="totalItems"
    :items-per-page="itemsPerPage"
    :page="page"
    :has-results="maps.length > 0"
    :loading="loading"
    empty-icon="pi pi-map"
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
          v-for="map in maps"
          :key="map.id"
          :object-type="'map'"
          :title="map.title"
          :summary="map.description"
          :thumbnail="map.thumbnail"
          :show-thumbnail="true"
          :object-url="`/atlas/maps/${map.slug}`"
        />
      </div>
    </template>
  </PortalOverviewTemplate>
</template>

<script setup lang="ts">
import PortalCard from "@/portal/components/PortalCard.vue";
import PortalOverviewTemplate from "@/portal/components/PortalOverviewTemplate.vue";
import { onMounted, ref } from "vue";
import type { PageState } from "primevue/paginator";
import Dropdown from "primevue/dropdown";

interface Map {
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
const maps = ref<Map[]>([]);
const searchQuery = ref("");
const selectedSort = ref("title");
const page = ref(1);
const itemsPerPage = ref(12);
const totalItems = ref(0);

const sortOptions: SortOption[] = [
  { label: "Titel (A-Z)", value: "title" },
  { label: "Titel (Z-A)", value: "-title" },
];

const getMaps = async () => {
  loading.value = true;
  const params = new URLSearchParams();
  params.set("published", "True");
  params.set("show_in_overview", "True");
  if (searchQuery.value) params.set("search", searchQuery.value);
  params.set("page", page.value.toString());
  params.set("page_size", itemsPerPage.value.toString());
  if (selectedSort.value) params.set("ordering", selectedSort.value);

  try {
    const res = await fetch(`/atlas/api/v1/maps/?${params}`, {
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
    });
    if (!res.ok) {
      console.error("Could not fetch maps");
      return;
    }
    const data = await res.json();
    maps.value = data.results || [];
    totalItems.value = data.count ?? 0;
  } catch (e) {
    console.error("Error fetching maps:", e);
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  page.value = 1;
  getMaps();
};

const handleSortChange = () => {
  page.value = 1;
  getMaps();
};

const handleItemsPerPageChange = (v: number) => {
  itemsPerPage.value = v;
  page.value = 1;
  getMaps();
};

const updatePageState = (pageState: PageState) => {
  page.value = pageState.page + 1;
  itemsPerPage.value = pageState.rows;
  getMaps();
};

onMounted(() => {
  getMaps();
});
</script>
