<template>
  <PortalOverviewTemplate
    v-model:search-query="searchQuery"
    title="Metadatasets"
    subtitle="Doorzoek alle beschikbare metadatasets in het dataportaal. Gebruik filters om je zoekopdracht te verfijnen."
    header-icon="pi pi-database"
    search-placeholder="Zoek op naam, trefwoord of categorie..."
    :total-records="totalItems"
    :items-per-page="itemsPerPage"
    :page="page"
    :has-results="metadatasets.length > 0"
    empty-icon="pi pi-database"
    empty-title="Geen resultaten gevonden"
    empty-message="Probeer andere zoektermen of filters om resultaten te vinden."
    @search="handleSearch"
    @update:items-per-page="handleItemsPerPageChange"
    @page="updatePageState"
  >
    <template #filters>
      <div class="tw-grid md:tw-grid-cols-2 tw-gap-6">
        <div>
          <label class="tw-block tw-text-sm tw-font-medium tw-text-gray-700 tw-mb-2"> Onderwerp </label>
          <PortalTopicSelect :selected-topic="selectedTopic" @on-topic-change="setSelectedTopic" />
        </div>
        <div>
          <label class="tw-block tw-text-sm tw-font-medium tw-text-gray-700 tw-mb-2"> Sorteren op </label>
          <PortalSortSelect :selected-sort="selectedSort" @on-sort-change="setSelectedSort" />
        </div>
      </div>
    </template>

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
import PortalSortSelect from "@/portal/components/PortalSortSelect.vue";
import PortalTopicSelect from "@/portal/components/PortalTopicSelect.vue";
import { APIResponseType } from "@/types/APIResponseType";
import { IMetadataset } from "@/types/metadataset";
import { topicCategoryLabels } from "@/types/TopicCategory";
import type { TopicCategoryId } from "@/types/TopicCategory";
import { computed, onMounted, ref } from "vue";
import { useGlobalStore } from "@/stores";
import type { PageState } from "primevue/paginator";

const metadatasets = ref<IMetadataset[]>([]);
const searchQuery = ref<string>("");
const selectedTopic = ref<string>("");
const selectedSort = ref<string>("title");
const page = ref<number>(1);
const itemsPerPage = ref<number>(12);
const totalItems = ref<number>(0);

const globalStore = useGlobalStore();
const user = computed(() => globalStore.user);

const getMetadatasets = async (): Promise<void> => {
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
      console.error("Could not fetch metadatasets");
      return;
    }

    const response: APIResponseType<IMetadataset> = await result.json();
    metadatasets.value = response.results;
    totalItems.value = response.count;
  } catch (error) {
    console.error("Error fetching metadatasets:", error);
  }
};

const handleSearch = () => {
  page.value = 1;
  getMetadatasets();
};

const setSelectedTopic = (topic: string) => {
  selectedTopic.value = topic;
  page.value = 1;
  getMetadatasets();
};

const setSelectedSort = (sort: string) => {
  selectedSort.value = sort;
  page.value = 1;
  getMetadatasets();
};

const handleItemsPerPageChange = (v: number) => {
  itemsPerPage.value = v;
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
  getMetadatasets();
});
</script>
