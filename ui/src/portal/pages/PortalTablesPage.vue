<template>
  <PortalOverviewTemplate
    v-model:search-query="searchQuery"
    :view-mode="viewMode"
    title="Tabellen"
    subtitle="Doorzoek alle beschikbare tabellen in het dataportaal. Gebruik de zoekfunctie om tabellen te vinden."
    header-icon="pi pi-chart-bar"
    search-placeholder="Zoek op tabellen..."
    :total-records="totalItems"
    :items-per-page="itemsPerPage"
    :page="page"
    :has-results="tables.length > 0"
    :loading="loading"
    :error="error"
    empty-icon="pi pi-chart-bar"
    empty-title="Geen resultaten gevonden"
    empty-message="Probeer andere zoektermen om resultaten te vinden."
    @update:view-mode="handleViewModeChange"
    @search="handleSearch"
    @update:items-per-page="handleItemsPerPageChange"
    @page="updatePageState"
  >
    <template #filters>
      <div class="tw-grid md:tw-grid-cols-2 tw-gap-6">
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
        <div v-for="table in tables" :key="table.id" class="tw-relative">
          <PortalCard
            :object-type="PortalCardObjectType.Table"
            :layout-mode="viewMode"
            :title="table.title"
            :summary="table.description"
            :thumbnail="null"
            :show-thumbnail="false"
            :object-url="`/tables/${table.slug}`"
            :last-updated="null"
            :category="null"
          />
          <span v-if="isInternal(table) && user" class="tw-absolute tw-top-3 tw-right-3 tw-z-10">
            <VisibilityIndicator visibility="Intern" />
          </span>
        </div>
      </div>
    </template>
  </PortalOverviewTemplate>
</template>

<script setup lang="ts">
import PortalCard from "@/portal/components/PortalCard.vue";
import PortalOverviewTemplate from "@/portal/components/PortalOverviewTemplate.vue";
import VisibilityIndicator from "@/components/VisibilityIndicator.vue";
import { LayoutMode, PortalCardObjectType, SortOrder } from "@/portal/components/shared/portalCardShared";
import type { IPortalTable } from "@/types/table";
import { useGlobalStore } from "@/stores";
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import type { PageState } from "primevue/paginator";
import Dropdown from "primevue/dropdown";
import { usePortalQueryParams } from "@/portal/composables/usePortalQueryParams";

interface SortOption {
  label: string;
  value: SortOrder;
}

const route = useRoute();
const { parseFromUrl, syncToUrl } = usePortalQueryParams();
const globalStore = useGlobalStore();
const user = computed(() => globalStore.user);
const loading = ref(false);
const error = ref<string | null>(null);
const tables = ref<IPortalTable[]>([]);
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

const isInternal = (table: IPortalTable): boolean => {
  return !!table.login_required || !!table.only_internal;
};

const getTables = async () => {
  loading.value = true;
  error.value = null;
  const params = new URLSearchParams();
  if (searchQuery.value) params.set("search", searchQuery.value);
  params.set("page", page.value.toString());
  params.set("page_size", itemsPerPage.value.toString());
  if (selectedSort.value) params.set("ordering", selectedSort.value as string);

  try {
    // TODO: replace with new tables
    const res = await fetch(`/atlas/api/v1/tables_old/?${params.toString()}`, {
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
    });
    if (!res.ok) {
      error.value = "Kon tabellen niet laden. Probeer het opnieuw.";
      return;
    }
    const data = await res.json();
    tables.value = data.results || [];
    totalItems.value = data.count ?? 0;
  } catch (e) {
    console.error("Error fetching tables:", e);
    error.value = "Er is een probleem opgetreden bij het laden van de tabellen.";
  } finally {
    loading.value = false;
  }
};

const syncUrl = () => {
  syncToUrl({
    query: searchQuery.value,
    page: page.value,
    page_size: itemsPerPage.value,
    sort: selectedSort.value,
    view: viewMode.value,
  });
};

const handleSearch = () => {
  page.value = 1;
  syncUrl();
  getTables();
};

const handleSortChange = () => {
  page.value = 1;
  syncUrl();
  getTables();
};

const handleItemsPerPageChange = (v: number) => {
  itemsPerPage.value = v;
  page.value = 1;
  syncUrl();
  getTables();
};

const updatePageState = (pageState: PageState) => {
  page.value = pageState.page + 1;
  itemsPerPage.value = pageState.rows;
  syncUrl();
  getTables();
};

const handleViewModeChange = (v: LayoutMode) => {
  viewMode.value = v;
  syncToUrl({ view: v });
};

const applyParamsFromUrl = (): void => {
  const params = parseFromUrl();
  searchQuery.value = params.query ?? "";
  selectedSort.value = (params.sort ?? SortOrder.TitleAsc) as SortOrder;
  page.value = params.page ?? 1;
  itemsPerPage.value = params.page_size ?? 12;
  viewMode.value = params.view ?? LayoutMode.Grid;
};

const routeQueryKey = computed(() => JSON.stringify(route.query));

watch(
  routeQueryKey,
  () => {
    applyParamsFromUrl();
    getTables();
  },
  { immediate: true },
);
</script>
