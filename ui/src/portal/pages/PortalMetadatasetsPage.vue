<template>
  <PortalOverviewTemplate
    v-model:search-query="searchQuery"
    :view-mode="viewMode"
    title="Metadatasets"
    subtitle="Doorzoek alle beschikbare metadatasets in het dataportaal. Gebruik filters om je zoekopdracht te verfijnen."
    header-icon="pi pi-database"
    search-placeholder="Zoek op naam, trefwoord of categorie..."
    :total-records="totalItems"
    :items-per-page="itemsPerPage"
    :page="page"
    :has-results="metadatasets.length > 0"
    :loading="loading"
    :error="error"
    empty-icon="pi pi-database"
    empty-title="Geen resultaten gevonden"
    empty-message="Probeer andere zoektermen of filters om resultaten te vinden."
    @update:view-mode="handleViewModeChange"
    @search="handleSearch"
    @update:items-per-page="handleItemsPerPageChange"
    @page="updatePageState"
  >
    <template #filters>
      <div class="tw-flex tw-flex-col tw-gap-6">
        <div>
          <label class="tw-block tw-text-sm tw-font-medium tw-text-[var(--color-text-organization)] tw-mb-2">
            Onderwerp
          </label>
          <PortalTopicSelect :selected-topic="selectedTopic" @on-topic-change="setSelectedTopic" />
        </div>
        <div>
          <label class="tw-block tw-text-sm tw-font-medium tw-text-[var(--color-text-organization)] tw-mb-2">
            Sorteren op
          </label>
          <PortalSortSelect :selected-sort="selectedSort" @on-sort-change="setSelectedSort" />
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
        <div v-for="metadataset in metadatasets" :key="metadataset.id" class="tw-relative">
          <PortalCard
            :object-type="PortalCardObjectType.Metadataset"
            :layout-mode="viewMode"
            :title="metadataset.title"
            :summary="metadataset.abstract || metadataset.description || ''"
            :thumbnail="null"
            :show-thumbnail="false"
            :object-url="`/metadatasets/${metadataset.slug}`"
            :last-updated="metadataset.last_updated ?? null"
            :category="getTopicCategoryLabel(metadataset.topic_category) || null"
          />
          <span v-if="isInternal(metadataset) && user" class="tw-absolute tw-top-3 tw-right-3 tw-z-10">
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
import PortalSortSelect from "@/portal/components/PortalSortSelect.vue";
import PortalTopicSelect from "@/portal/components/PortalTopicSelect.vue";
import VisibilityIndicator from "@/components/VisibilityIndicator.vue";
import { LayoutMode, PortalCardObjectType, SortOrder } from "@/portal/components/shared/portalCardShared";
import { APIResponseType } from "@/types/APIResponseType";
import { IMetadataset } from "@/types/metadataset";
import { topicCategoryLabels } from "@/types/TopicCategory";
import type { TopicCategoryId } from "@/types/TopicCategory";
import { computed, ref, watch } from "vue";
import { useRoute } from "vue-router";
import { useGlobalStore } from "@/stores";
import type { PageState } from "primevue/paginator";
import { usePortalQueryParams } from "@/portal/composables/usePortalQueryParams";

const metadatasets = ref<IMetadataset[]>([]);
const loading = ref(false);
const error = ref<string | null>(null);
const searchQuery = ref<string>("");
const selectedTopic = ref<string>("");
const selectedSort = ref<SortOrder>(SortOrder.TitleAsc);
const page = ref<number>(1);
const itemsPerPage = ref<number>(12);
const totalItems = ref<number>(0);
const viewMode = ref<LayoutMode>(LayoutMode.Grid);

const route = useRoute();
const { parseFromUrl, syncToUrl } = usePortalQueryParams();
const globalStore = useGlobalStore();
const user = computed(() => globalStore.user);

const getMetadatasets = async (): Promise<void> => {
  loading.value = true;
  error.value = null;
  const searchParams = new URLSearchParams();

  if (!user.value) {
    searchParams.set("status", "completed");
    searchParams.set("show_in_overview", "True");
  }

  if (searchQuery.value) searchParams.set("search", searchQuery.value);
  if (selectedTopic.value) searchParams.set("topic_category", selectedTopic.value);
  if (selectedSort.value) searchParams.set("ordering", selectedSort.value);
  searchParams.set("page", page.value.toString());
  searchParams.set("page_size", itemsPerPage.value.toString());

  try {
    const result = await fetch(`/atlas/api/v1/metadatasets/?${searchParams.toString()}`, {
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
    });

    if (!result.ok) {
      error.value = "Kon metadatasets niet laden. Probeer het opnieuw.";
      return;
    }

    const response: APIResponseType<IMetadataset> = await result.json();
    metadatasets.value = response.results;
    totalItems.value = response.count;
  } catch (err) {
    console.error("Error fetching metadatasets:", err);
    error.value = "Er is een probleem opgetreden bij het laden van de metadatasets.";
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
    topic: selectedTopic.value,
  });
};

const handleSearch = () => {
  page.value = 1;
  syncUrl();
  getMetadatasets();
};

const setSelectedTopic = (topic: string) => {
  selectedTopic.value = topic;
  page.value = 1;
  syncUrl();
  getMetadatasets();
};

const setSelectedSort = (sort: string) => {
  selectedSort.value = sort as SortOrder;
  page.value = 1;
  syncUrl();
  getMetadatasets();
};

const handleItemsPerPageChange = (v: number) => {
  itemsPerPage.value = v;
  page.value = 1;
  syncUrl();
  getMetadatasets();
};

const updatePageState = (pageState: PageState) => {
  page.value = pageState.page + 1;
  itemsPerPage.value = pageState.rows;
  syncUrl();
  getMetadatasets();
};

const handleViewModeChange = (v: LayoutMode) => {
  viewMode.value = v;
  syncToUrl({ view: v });
};

const isInternal = (metadataset: IMetadataset): boolean => {
  return metadataset.authorization_level === "internal" || !metadataset.show_in_overview;
};

const getTopicCategoryLabel = (topicId: string): string => {
  return topicCategoryLabels[topicId as TopicCategoryId] || topicId || "";
};

const applyParamsFromUrl = (): void => {
  const params = parseFromUrl();
  searchQuery.value = params.query ?? "";
  selectedTopic.value = params.topic ?? "";
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
    getMetadatasets();
  },
  { immediate: true },
);
</script>
