<template>
  <div class="tw-mx-auto tw-max-w-7xl tw-px-4 md:tw-pt-6 tw-my-4 tw-w-full">
    <h1 class="tw-text-2xl md:tw-text-4xl tw-my-0 tw-mb-2">
      Alle zoekresultaten voor: "{{ searchQuery }}" ({{ totalItems }} resultaten)
    </h1>
    <section class="tw-flex-1">
      <div class="tw-w-full md:tw-w-2/6 tw-my-5">
        <PortalSearchField :initial-search-query="searchQuery" @on-search="onSearch" />
      </div>
      <div v-if="results > 0">
        <div v-if="metadatasets.length > 0">
          <h3 class="tw-m-0 tw-text-3xl md:tw-mt-6 md:tw-mb-2">Metadatasets</h3>
          <PortalMetadatasetList :metadatasets="metadatasets" />
          <div class="tw-flex tw-flex-row tw-items-start tw-py-8">
            <Paginator
              :first="(page - 1) * itemsPerPage"
              :rows="itemsPerPage"
              :total-records="totalItems"
              @page="updatePageState"
            />
          </div>
        </div>
      </div>
      <div v-else class="tw-mt-4">
        <p>Helaas er zijn geen resultaten gevonden voor de zoekopdracht: "{{ searchQuery }}"</p>
      </div>
    </section>
  </div>
</template>

<script setup lang="ts">
import PortalMetadatasetList from "@/portal/components/dataset/PortalMetadatasetList.vue";
import PortalSearchField from "@/portal/components/PortalSearchField.vue";
import { APIResponseType } from "@/types/APIResponseType";
import type { IMetadataset } from "@/types/metadataset";
import { computed, onMounted, ref } from "vue";
import { useRoute, useRouter } from "vue-router";
import { useGlobalStore } from "@/stores";
import type { PageState } from "primevue/paginator";

const route = useRoute();
const router = useRouter();

const metadatasets = ref<IMetadataset[]>([]);
const searchQuery = ref<string>("");

const page = ref<number>(1);
const itemsPerPage = ref<number>(20);
const totalItems = ref<number>(0);

const globalStore = useGlobalStore();
const user = computed(() => globalStore.user);

const results = computed((): number => {
  return metadatasets.value.length;
});

const getMetadatasets = async (): Promise<void> => {
  try {
    // For logged-in users, show all metadatasets regardless of status and show_in_overview
    // For anonymous users, only show completed metadatasets that are marked for overview
    const searchParams = new URLSearchParams();

    // Anonymous users see only public metadatasets
    if (!user.value) {
      searchParams.set("status", "completed");
      searchParams.set("show_in_overview", "True");
    }

    searchParams.set("search", searchQuery.value);
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
  }
};

const onSearch = (query: string) => {
  searchQuery.value = query;
  page.value = 1;
  router.push({ query: { query } });
  getMetadatasets();
};

const updatePageState = (pageState: PageState) => {
  page.value = pageState.page + 1;
  itemsPerPage.value = pageState.rows;
  getMetadatasets();
};

onMounted(() => {
  searchQuery.value = (route.query.query as string) || "";
  getMetadatasets();
});
</script>
