<template>
  <div class="container __portal">
    <h1 class="__portal">Metadatasets ({{ totalItems }})</h1>
    <section>
      <div class="tw-flex tw-flex-col tw-gap-4 tw-mb-6">
        <div class="tw-w-full">
          <PortalSearchField :initial-search-query="searchQuery" @on-search="setSearchQuery" />
        </div>
        <div
          class="tw-flex tw-gap-4 tw-items-center tw-flex-wrap md:tw-flex-row tw-flex-col md:tw-items-center tw-items-stretch"
        >
          <PortalTopicSelect :selected-topic="selectedTopic" @on-topic-change="setSelectedTopic" />
          <PortalSortSelect :selected-sort="selectedSort" @on-sort-change="setSelectedSort" />
        </div>
      </div>
      <PortalMetadatasetList :metadatasets="metadatasets" />
      <div v-if="metadatasets.length === 0">
        <p>Geen metadatasets gevonden</p>
      </div>
      <div v-if="metadatasets.length > 0" class="tw-flex tw-flex-row tw-items-start tw-py-8">
        <Paginator
          :first="(page - 1) * itemsPerPage"
          :rows="itemsPerPage"
          :total-records="totalItems"
          @page="updatePageState"
        />
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import PortalMetadatasetList from "@/portal/components/dataset/PortalMetadatasetList.vue";
import PortalSearchField from "@/portal/components/PortalSearchField.vue";
import PortalSortSelect from "@/portal/components/PortalSortSelect.vue";
import PortalTopicSelect from "@/portal/components/PortalTopicSelect.vue";
import { APIResponseType } from "@/types/APIResponseType";
import { IMetadataset } from "@/types/metadataset";
import { computed, onMounted, ref } from "vue";
import { useGlobalStore } from "@/stores";
import type { PageState } from "primevue/paginator";

const metadatasets = ref<IMetadataset[]>([]);
const searchQuery = ref<string>("");
const selectedTopic = ref<string>("");
const selectedSort = ref<string>("title");
const page = ref<number>(1);
const itemsPerPage = ref<number>(20);
const totalItems = ref<number>(0);

const globalStore = useGlobalStore();
const user = computed(() => globalStore.user);

const getMetadatasets = async (): Promise<void> => {
  const searchParams = new URLSearchParams();

  // For logged-in users, show all metadatasets regardless of status and show_in_overview
  // For anonymous users, only show completed metadatasets that are marked for overview
  if (!user.value) {
    searchParams.set("status", "completed");
    searchParams.set("show_in_overview", "True");
  }

  if (searchQuery.value) searchParams.set("search", searchQuery.value);
  if (selectedTopic.value) searchParams.set("topic_category", selectedTopic.value);
  if (selectedSort.value) searchParams.set("ordering", selectedSort.value);

  // Add pagination parameters
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

const setSearchQuery = (query: string) => {
  searchQuery.value = query;
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

const updatePageState = (pageState: PageState) => {
  page.value = pageState.page + 1;
  itemsPerPage.value = pageState.rows;
  getMetadatasets();
};

onMounted(() => {
  getMetadatasets();
});
</script>
