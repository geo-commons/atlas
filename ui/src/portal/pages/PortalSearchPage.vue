<template>
  <PortalOverviewTemplate
    v-model:search-query="searchQuery"
    title="Zoekresultaten"
    :subtitle="subtitle"
    header-icon="pi pi-search"
    search-placeholder="Zoek op naam, trefwoord of categorie..."
    :total-records="totalItems"
    :items-per-page="itemsPerPage"
    :page="page"
    :has-results="metadatasets.length > 0"
    :loading="loading"
    empty-icon="pi pi-search"
    empty-title="Geen resultaten gevonden"
    :empty-message="emptyMessage"
    @search="handleSearch"
    @update:items-per-page="handleItemsPerPageChange"
    @page="updatePageState"
  >
    <template #default>
      <div class="tw-grid sm:tw-grid-cols-2 lg:tw-grid-cols-3 tw-gap-6 tw-mb-12">
        <div v-for="metadataset in metadatasets" :key="metadataset.id" class="tw-relative">
          <PortalCard
            :object-type="'metadataset'"
            :title="metadataset.title"
            :summary="metadataset.abstract || metadataset.description || ''"
            :show-thumbnail="false"
            :object-url="`/metadatasets/${metadataset.slug}`"
            :last-updated="metadataset.last_updated || undefined"
            :category="getTopicCategoryLabel(metadataset.topic_category)"
          />
          <span
            v-if="isInternal(metadataset) && user"
            class="tw-absolute tw-top-3 tw-right-3 tw-inline-block tw-px-2 tw-py-0.5 tw-text-xs tw-bg-white/90 tw-backdrop-blur-sm tw-text-gray-700 tw-rounded tw-font-medium tw-z-10"
          >
            Intern
          </span>
        </div>
      </div>
    </template>
  </PortalOverviewTemplate>
</template>

<script setup lang="ts">
import PortalCard from "@/portal/components/PortalCard.vue";
import PortalOverviewTemplate from "@/portal/components/PortalOverviewTemplate.vue";
import { APIResponseType } from "@/types/APIResponseType";
import type { IMetadataset } from "@/types/metadataset";
import { computed, onMounted, ref, watch } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useGlobalStore } from "@/stores";
import type { PageState } from "primevue/paginator";
import { topicCategoryLabels } from "@/types/TopicCategory";
import type { TopicCategoryId } from "@/types/TopicCategory";

const route = useRoute();
const router = useRouter();

const metadatasets = ref<IMetadataset[]>([]);
const searchQuery = ref<string>("");
const submittedQuery = ref<string>("");
const loading = ref(false);

const page = ref<number>(1);
const itemsPerPage = ref<number>(12);
const totalItems = ref<number>(0);

const globalStore = useGlobalStore();
const user = computed(() => globalStore.user);

const subtitle = computed((): string => {
  if (submittedQuery.value) {
    return `Resultaten voor "${submittedQuery.value}"`;
  }
  return "Doorzoek alle metadatasets in het dataportaal.";
});

const emptyMessage = computed((): string => {
  if (submittedQuery.value) {
    return `Geen resultaten gevonden voor "${submittedQuery.value}". Probeer andere zoektermen.`;
  }
  return "Er zijn geen resultaten beschikbaar. Probeer een andere zoekopdracht.";
});

const getMetadatasets = async (): Promise<void> => {
  loading.value = true;
  try {
    // For logged-in users, show all metadatasets regardless of status and show_in_overview
    // For anonymous users, only show completed metadatasets that are marked for overview
    const searchParams = new URLSearchParams();

    // Anonymous users see only public metadatasets
    if (!user.value) {
      searchParams.set("status", "completed");
      searchParams.set("show_in_overview", "True");
    }

    if (searchQuery.value) {
      searchParams.set("search", searchQuery.value);
    }
    searchParams.set("page", page.value.toString());
    searchParams.set("page_size", itemsPerPage.value.toString());

    const result = await fetch(`/atlas/api/v1/metadatasets/?${searchParams.toString()}`, {
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
    });

    if (!result.ok) {
      console.error("Could not fetch metadatasets");
      return;
    }

    const response: APIResponseType<IMetadataset> = await result.json();
    metadatasets.value = response.results;
    totalItems.value = response.count;
  } catch (error) {
    console.error("Error fetching metadatasets:", error);
  } finally {
    loading.value = false;
  }
};

const handleSearch = () => {
  page.value = 1;
  submittedQuery.value = searchQuery.value;
  router.push({ query: searchQuery.value ? { query: searchQuery.value } : {} });
  getMetadatasets();
};

const handleItemsPerPageChange = (value: number) => {
  itemsPerPage.value = value;
  page.value = 1;
  getMetadatasets();
};

const updatePageState = (pageState: PageState) => {
  page.value = pageState.page + 1;
  itemsPerPage.value = pageState.rows;
  getMetadatasets();
};

const isInternal = (metadataset: IMetadataset): boolean => {
  return metadataset.authorization_level === "internal";
};

const getTopicCategoryLabel = (topicId: string): string => {
  return topicCategoryLabels[topicId as TopicCategoryId] || topicId || "";
};

onMounted(() => {
  const initialQuery = (route.query.query as string) || "";
  searchQuery.value = initialQuery;
  submittedQuery.value = initialQuery;
  getMetadatasets();
});

watch(
  () => route.query.query,
  (value) => {
    const nextQuery = (value as string) || "";
    if (nextQuery !== searchQuery.value) {
      searchQuery.value = nextQuery;
      submittedQuery.value = nextQuery;
      page.value = 1;
      getMetadatasets();
    }
  },
);
</script>
