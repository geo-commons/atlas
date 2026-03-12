<template>
  <PortalOverviewTemplate
    v-model:search-query="searchQuery"
    :view-mode="viewMode"
    title="Kaarten"
    subtitle="Doorzoek alle beschikbare themakaarten in het dataportaal. Gebruik de zoekfunctie om kaarten te vinden."
    header-icon="pi pi-map"
    search-placeholder="Zoek op kaarten..."
    :total-records="totalItems"
    :items-per-page="itemsPerPage"
    :page="page"
    :has-results="maps.length > 0"
    :loading="loading"
    :error="error"
    empty-icon="pi pi-map"
    empty-title="Geen resultaten gevonden"
    empty-message="Probeer andere zoektermen om resultaten te vinden."
    @update:view-mode="handleViewModeChange"
    @search="handleSearch"
    @update:items-per-page="handleItemsPerPageChange"
    @page="updatePageState"
  >
    <template #filters>
      <div class="tw-flex tw-flex-col tw-gap-6">
        <div>
          <label class="tw-block tw-text-sm tw-font-medium tw-text-[var(--color-text-organization)] tw-mb-2"
            >Sorteren op</label
          >
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
      <div
        :class="[
          viewMode === LayoutMode.Grid
            ? 'tw-grid sm:tw-grid-cols-2 lg:tw-grid-cols-3 tw-gap-6'
            : 'tw-flex tw-flex-col tw-gap-4',
          'tw-mb-12',
        ]"
      >
        <PortalCard
          v-for="map in maps"
          :key="map.id"
          :object-type="PortalCardObjectType.Map"
          :layout-mode="viewMode"
          :title="map.title"
          :summary="map.description ?? null"
          :thumbnail="map.thumbnail ?? null"
          :show-thumbnail="true"
          :object-url="`/atlas/maps/${map.slug}`"
          :last-updated="null"
          :category="null"
        />
      </div>
    </template>
  </PortalOverviewTemplate>
</template>

<script setup lang="ts">
import PortalCard from "@/portal/components/PortalCard.vue";
import PortalOverviewTemplate from "@/portal/components/PortalOverviewTemplate.vue";
import { LayoutMode, PortalCardObjectType, SortOrder } from "@/portal/components/shared/portalCardShared";
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import type { PageState } from "primevue/paginator";
import Dropdown from "primevue/dropdown";
import { usePortalQueryParams } from "@/portal/composables/usePortalQueryParams";

interface Map {
  id: number;
  title: string;
  description?: string;
  slug: string;
  thumbnail?: string;
}

interface SortOption {
  label: string;
  value: SortOrder;
}

const route = useRoute();
const { parseFromUrl, syncToUrl } = usePortalQueryParams();
const loading = ref(false);
const error = ref<string | null>(null);
const maps = ref<Map[]>([]);
const searchQuery = ref("");
const selectedSort = ref<SortOrder>(SortOrder.TitleAsc);
const page = ref(1);
const itemsPerPage = ref(12);
const totalItems = ref(0);
const viewMode = ref<LayoutMode>(LayoutMode.Grid);

const sortOptions: SortOption[] = [
  { label: "Titel (A-Z)", value: SortOrder.TitleAsc },
  { label: "Titel (Z-A)", value: SortOrder.TitleDesc },
];

const getMaps = async (): Promise<void> => {
  loading.value = true;
  error.value = null;
  const params = new URLSearchParams();
  params.set("published", "True");
  params.set("show_in_overview", "True");
  if (searchQuery.value) params.set("search", searchQuery.value);
  params.set("page", page.value.toString());
  params.set("page_size", itemsPerPage.value.toString());
  if (selectedSort.value) params.set("ordering", selectedSort.value as string);

  try {
    const res = await fetch(`/atlas/api/v1/maps/?${params.toString()}`, {
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
    });
    if (!res.ok) {
      error.value = "Kon kaarten niet laden. Probeer het opnieuw.";
      return;
    }
    const data = await res.json();
    maps.value = data.results || [];
    totalItems.value = data.count ?? 0;
  } catch {
    error.value = "Er is een probleem opgetreden bij het laden van de kaarten.";
  } finally {
    loading.value = false;
  }
};

const syncUrl = (): void => {
  syncToUrl({
    query: searchQuery.value,
    page: page.value,
    page_size: itemsPerPage.value,
    sort: selectedSort.value,
    view: viewMode.value,
  });
};

const handleSearch = (): void => {
  page.value = 1;
  syncUrl();
  getMaps();
};

const handleSortChange = (): void => {
  page.value = 1;
  syncUrl();
  getMaps();
};

const handleItemsPerPageChange = (v: number): void => {
  itemsPerPage.value = v;
  page.value = 1;
  syncUrl();
  getMaps();
};

const updatePageState = (pageState: PageState): void => {
  page.value = pageState.page + 1;
  itemsPerPage.value = pageState.rows;
  syncUrl();
  getMaps();
};

const handleViewModeChange = (v: LayoutMode): void => {
  viewMode.value = v;
  syncToUrl({ view: v });
};

const applyParamsFromUrl = (): void => {
  const params = parseFromUrl();
  searchQuery.value = params.query;
  selectedSort.value = params.sort as SortOrder;
  page.value = params.page;
  itemsPerPage.value = params.page_size;
  viewMode.value = params.view;
};

const routeQueryKey = computed(() => JSON.stringify(route.query));

watch(
  routeQueryKey,
  () => {
    applyParamsFromUrl();
    getMaps();
  },
  { immediate: true },
);
</script>
