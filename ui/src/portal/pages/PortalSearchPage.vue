<template>
  <div class="tw-min-h-screen tw-bg-gray-50">
    <!-- Page Header -->
    <header class="tw-bg-white tw-border-b tw-border-gray-200 tw-border-solid tw-border-0">
      <div class="tw-max-w-7xl tw-mx-auto tw-px-6 tw-py-12">
        <div class="tw-flex tw-items-start tw-gap-4 tw-mb-4">
          <div
            class="tw-w-16 tw-h-16 tw-bg-gray-50 tw-rounded-2xl tw-flex tw-items-center tw-justify-center tw-flex-shrink-0"
          >
            <i class="pi pi-search tw-text-3xl tw-text-gray-700" aria-hidden="true"></i>
          </div>
          <div class="tw-flex-1">
            <h1 class="tw-text-4xl tw-my-3">Zoekresultaten</h1>
            <p class="tw-text-[var(--color-text-organization)] tw-text-lg tw-leading-relaxed tw-max-w-3xl">
              {{ subtitle }}
            </p>
          </div>
        </div>
      </div>
    </header>

    <!-- Main Content -->
    <main id="main-content" class="tw-max-w-7xl tw-mx-auto tw-px-6 tw-py-12">
      <!-- Search -->
      <div class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-p-8 tw-mb-10">
        <PortalSearchField
          :initial-search-query="searchQuery"
          placeholder="Zoek op naam, trefwoord of categorie..."
          @on-search="onSearchFromField"
        />
      </div>

      <Spinner v-if="loading" class="spinner" :style-type="'portal'" />

      <template v-else-if="hasAnyResults">
        <div class="tw-flex tw-items-center tw-justify-between tw-mb-8">
          <p class="tw-text-[var(--color-text-organization)]">
            <span class="tw-font-medium tw-text-[var(--color-text-organization)]">{{ totalResults }}</span>
            {{ totalResults === 1 ? "resultaat" : "resultaten" }} getoond
          </p>
          <div class="tw-flex tw-items-center tw-gap-2">
            <label class="tw-text-sm tw-text-[var(--color-text-organization)]" for="search-view-mode">Weergave:</label>
            <Dropdown
              :model-value="viewMode"
              :options="viewModeOptions"
              option-label="label"
              option-value="value"
              input-id="search-view-mode"
              :pt="{ input: { class: 'tw-text-sm' }, panel: { class: 'tw-text-sm' } }"
              @update:model-value="handleViewModeChange"
            />
          </div>
        </div>

        <!-- Metadatasets Section -->
        <section v-if="metadatasets.length > 0" class="tw-mb-16" aria-labelledby="section-metadatasets">
          <div class="tw-flex tw-items-center tw-justify-between">
            <h2
              id="section-metadatasets"
              class="tw-text-2xl tw-font-semibold tw-mb-6 tw-flex tw-items-center tw-gap-2 tw-flex-wrap"
            >
              <i class="pi pi-database tw-text-gray-600" aria-hidden="true"></i>
              Metadatasets
              <span class="tw-text-base tw-font-normal tw-text-[var(--color-text-organization)]">
                ({{ metadatasetsCount }})
              </span>
            </h2>
          </div>
          <div
            :class="[
              viewMode === LayoutMode.Grid
                ? 'tw-grid sm:tw-grid-cols-2 lg:tw-grid-cols-3 tw-gap-6'
                : 'tw-flex tw-flex-col tw-gap-4',
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

            <a
              v-if="metadatasets.length < metadatasetsCount"
              :href="metadatasetsAllUrl"
              class="tw-text-[var(--color-primary-organization)] hover:tw-opacity-80 tw-transition-colors tw-font-medium tw-text-lg tw-flex tw-items-center tw-gap-1 tw-no-underline tw-ml-2 focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-[var(--color-primary-organization)] focus-visible:tw-ring-offset-2"
            >
              Bekijk alle {{ metadatasetsCount }} resultaten <i class="pi pi-arrow-right" aria-hidden="true"></i>
            </a>
          </div>
        </section>

        <!-- Maps Section -->
        <section v-if="maps.length > 0" class="tw-mb-16" aria-labelledby="section-maps">
          <div class="tw-flex tw-items-center tw-justify-between">
            <h2
              id="section-maps"
              class="tw-text-2xl tw-font-semibold tw-mb-6 tw-flex tw-items-center tw-gap-2 tw-flex-wrap"
            >
              <i class="pi pi-map tw-text-gray-600" aria-hidden="true"></i>
              Kaarten
              <span class="tw-text-base tw-font-normal tw-text-[var(--color-text-organization)]">
                ({{ mapsCount }})
              </span>
            </h2>
          </div>
          <div
            :class="[
              viewMode === LayoutMode.Grid
                ? 'tw-grid sm:tw-grid-cols-2 lg:tw-grid-cols-3 tw-gap-6'
                : 'tw-flex tw-flex-col tw-gap-4',
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

          <a
            v-if="maps.length < mapsCount"
            :href="mapsAllUrl"
            class="tw-mt-6 tw-text-[var(--color-primary-organization)] hover:tw-opacity-80 tw-transition-colors tw-font-medium tw-text-lg tw-flex tw-items-center tw-gap-1 tw-no-underline tw-ml-2 focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-[var(--color-primary-organization)] focus-visible:tw-ring-offset-2"
          >
            Bekijk alle {{ mapsCount }} resultaten <i class="pi pi-arrow-right" aria-hidden="true"></i>
          </a>
        </section>

        <!-- Tables Section -->
        <section v-if="tables.length > 0" class="tw-mb-16" aria-labelledby="section-tables">
          <div class="tw-flex tw-items-center tw-justify-between">
            <h2
              id="section-tables"
              class="tw-text-2xl tw-font-semibold tw-mb-6 tw-flex tw-items-center tw-gap-2 tw-flex-wrap"
            >
              <i class="pi pi-table tw-text-gray-600" aria-hidden="true"></i>
              Tabellen
              <span class="tw-text-base tw-font-normal tw-text-[var(--color-text-organization)]">
                ({{ tablesCount }})
              </span>
            </h2>
          </div>
          <div
            :class="[
              viewMode === LayoutMode.Grid
                ? 'tw-grid sm:tw-grid-cols-2 lg:tw-grid-cols-3 tw-gap-6'
                : 'tw-flex tw-flex-col tw-gap-4',
            ]"
          >
            <div v-for="table in tables" :key="table.slug" class="tw-relative">
              <PortalCard
                :object-type="PortalCardObjectType.Table"
                :layout-mode="viewMode"
                :title="table.title"
                :summary="null"
                :thumbnail="null"
                :show-thumbnail="false"
                :object-url="`/tables/${table.slug}`"
                :last-updated="null"
                :category="null"
              />
              <span
                v-if="table.show_in_portal && table.login_required && user"
                class="tw-absolute tw-top-3 tw-right-3 tw-z-10"
              >
                <VisibilityIndicator visibility="Intern" />
              </span>
            </div>
          </div>

          <a
            v-if="tables.length < tablesCount"
            :href="tablesAllUrl"
            class="tw-mt-6 tw-text-[var(--color-primary-organization)] hover:tw-opacity-80 tw-transition-colors tw-font-medium tw-text-lg tw-flex tw-items-center tw-gap-1 tw-no-underline tw-ml-2 focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-[var(--color-primary-organization)] focus-visible:tw-ring-offset-2"
          >
            Bekijk alle {{ tablesCount }} resultaten <i class="pi pi-arrow-right" aria-hidden="true"></i>
          </a>
        </section>
      </template>

      <!-- Error State -->
      <div
        v-else-if="hasErrors"
        class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-p-16 tw-text-center"
      >
        <i
          class="pi pi-exclamation-triangle tw-w-16 tw-h-16 tw-text-amber-500 tw-mx-auto tw-mb-4"
          aria-hidden="true"
        ></i>
        <h3 class="tw-text-xl tw-text-[var(--color-text-organization)] tw-mb-2 tw-font-medium">Laden mislukt</h3>
        <p class="tw-text-[var(--color-text-organization)] tw-max-w-md tw-mx-auto">
          {{ errorMessage }}
        </p>
      </div>

      <!-- Empty State -->
      <div v-else class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-p-16 tw-text-center">
        <i class="pi pi-search tw-w-16 tw-h-16 tw-text-gray-300 tw-mx-auto tw-mb-4" aria-hidden="true"></i>
        <h3 class="tw-text-xl tw-text-[var(--color-text-organization)] tw-mb-2 tw-font-medium">{{ emptyTitle }}</h3>
        <p class="tw-text-[var(--color-text-organization)] tw-max-w-md tw-mx-auto">
          {{ emptyMessage }}
        </p>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import PortalCard from "@/portal/components/PortalCard.vue";
import PortalSearchField from "@/portal/components/PortalSearchField.vue";
import Spinner from "@/components/Spinner.vue";
import VisibilityIndicator from "@/components/VisibilityIndicator.vue";
import Dropdown from "primevue/dropdown";
import { APIResponseType } from "@/types/APIResponseType";
import type { IMetadataset } from "@/types/metadataset";
import { computed, ref, watch } from "vue";
import { useRoute } from "@/utils/inertia-routing";
import { usePortalQueryParams } from "@/portal/composables/usePortalQueryParams";
import { useGlobalStore } from "@/stores";
import { topicCategoryLabels } from "@/types/TopicCategory";
import type { TopicCategoryId } from "@/types/TopicCategory";
import { LayoutMode, PortalCardObjectType } from "@/portal/components/shared/portalCardShared";
import { IRelatedTable } from "@/types/related-table";

interface Map {
  id: number;
  title: string;
  description?: string;
  slug: string;
  thumbnail?: string;
}

const route = useRoute();
const { parseFromUrl, syncToUrl } = usePortalQueryParams();
const globalStore = useGlobalStore();

const metadatasets = ref<IMetadataset[]>([]);
const maps = ref<Map[]>([]);
const tables = ref<IRelatedTable[]>([]);
const metadatasetsCount = ref<number>(0);
const mapsCount = ref<number>(0);
const tablesCount = ref<number>(0);
const searchQuery = ref<string>("");
const submittedQuery = ref<string>("");
const loading = ref(false);
const viewMode = ref<LayoutMode>(LayoutMode.Grid);
const errors = ref<{ metadatasets: string | null; maps: string | null; tables: string | null }>({
  metadatasets: null,
  maps: null,
  tables: null,
});

const user = computed(() => globalStore.user);

const totalResults = computed(() => metadatasets.value.length + maps.value.length + tables.value.length);
const hasAnyResults = computed(() => totalResults.value > 0);
const hasErrors = computed(() => !!(errors.value.metadatasets || errors.value.maps || errors.value.tables));
const errorMessage = computed(() => {
  const parts: string[] = [];
  if (errors.value.metadatasets) parts.push(errors.value.metadatasets);
  if (errors.value.maps) parts.push(errors.value.maps);
  if (errors.value.tables) parts.push(errors.value.tables);
  return parts.join(" ");
});

const metadatasetsAllUrl = computed(
  () => `/metadatasets${submittedQuery.value ? `?query=${encodeURIComponent(submittedQuery.value)}` : ""}`,
);
const mapsAllUrl = computed(
  () => `/maps${submittedQuery.value ? `?query=${encodeURIComponent(submittedQuery.value)}` : ""}`,
);
const tablesAllUrl = computed(
  () => `/tables${submittedQuery.value ? `?query=${encodeURIComponent(submittedQuery.value)}` : ""}`,
);

const subtitle = computed((): string => {
  if (submittedQuery.value) {
    return `Resultaten voor "${submittedQuery.value}"`;
  }
  return "Doorzoek metadatasets, kaarten en tabellen in het dataportaal.";
});

const emptyTitle = "Geen resultaten gevonden";
const emptyMessage = computed((): string => {
  if (submittedQuery.value) {
    return `Geen resultaten gevonden voor "${submittedQuery.value}". Probeer andere zoektermen.`;
  }
  return "Voer een zoekterm in om te zoeken in metadatasets, kaarten en tabellen.";
});

const viewModeOptions = [
  { label: "Grid", value: LayoutMode.Grid },
  { label: "Lijst", value: LayoutMode.List },
];

const getMetadatasets = async (): Promise<void> => {
  const searchParams = new URLSearchParams();
  if (!user.value) {
    searchParams.set("status", "completed");
    searchParams.set("show_in_overview", "True");
  }
  if (submittedQuery.value) {
    searchParams.set("search", submittedQuery.value);
  }
  searchParams.set("page", "1");
  searchParams.set("page_size", "12");

  const result = await fetch(`/atlas/api/v1/metadatasets/?${searchParams.toString()}`, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });
  if (!result.ok) {
    errors.value.metadatasets = "Kon metadatasets niet laden. Probeer het opnieuw.";
    return;
  }
  errors.value.metadatasets = null;
  const response: APIResponseType<IMetadataset> = await result.json();
  metadatasets.value = response.results;
  metadatasetsCount.value = response.count ?? 0;
};

const getMaps = async (): Promise<void> => {
  const params = new URLSearchParams();
  params.set("published", "True");
  params.set("show_in_overview", "True");
  if (submittedQuery.value) params.set("search", submittedQuery.value);
  params.set("page", "1");
  params.set("page_size", "12");

  const res = await fetch(`/atlas/api/v1/maps/?${params.toString()}`, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) {
    errors.value.maps = "Kon kaarten niet laden. Probeer het opnieuw.";
    return;
  }
  errors.value.maps = null;
  const data = await res.json();
  maps.value = data.results || [];
  mapsCount.value = data.count ?? 0;
};

const getTables = async (): Promise<void> => {
  const params = new URLSearchParams();
  if (submittedQuery.value) params.set("search", submittedQuery.value);
  params.set("page", "1");
  params.set("page_size", "12");

  const res = await fetch(`/atlas/api/v1/tables/?${params.toString()}&show_in_portal=True`, {
    credentials: "same-origin",
    headers: { "Content-Type": "application/json" },
  });
  if (!res.ok) {
    errors.value.tables = "Kon tabellen niet laden. Probeer het opnieuw.";
    tables.value = [];
    tablesCount.value = 0;
    return;
  }
  errors.value.tables = null;
  const data = await res.json();
  tables.value = data.results || [];
  tablesCount.value = data.count ?? 0;
};

const fetchAll = async (): Promise<void> => {
  loading.value = true;
  errors.value = { metadatasets: null, maps: null, tables: null };
  try {
    await Promise.all([getMetadatasets(), getMaps(), getTables()]);
  } catch (error) {
    console.error("Error fetching search results:", error);
    errors.value.metadatasets = errors.value.metadatasets || "Er is een probleem opgetreden bij het laden.";
  } finally {
    loading.value = false;
  }
};

const handleViewModeChange = (v: LayoutMode) => {
  viewMode.value = v;
  syncToUrl({ query: submittedQuery.value || undefined, view: v });
};

const onSearchFromField = (q: string) => {
  searchQuery.value = q;
  submittedQuery.value = q;
  syncToUrl({ query: q || undefined, view: viewMode.value });
  fetchAll();
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
  submittedQuery.value = params.query ?? "";
  viewMode.value = params.view ?? LayoutMode.Grid;
};

const routeQueryKey = computed(() => JSON.stringify(route.query));

watch(
  routeQueryKey,
  () => {
    applyParamsFromUrl();
    fetchAll();
  },
  { immediate: true },
);
</script>
