<template>
  <div class="tw-min-h-screen tw-bg-gray-50">
    <!-- Header Section -->
    <section class="tw-bg-white tw-border-b tw-border-gray-200 tw-border-solid tw-border-0">
      <div class="tw-max-w-7xl tw-mx-auto tw-px-6 tw-py-16">
        <div class="tw-grid md:tw-grid-cols-2 tw-gap-12 tw-items-stretch">
          <!-- Left: Text Content -->
          <div class="tw-flex tw-flex-col tw-justify-center">
            <h1 class="tw-text-5xl tw-mb-6 tw-leading-tight">
              {{ config?.organization_header ? config.organization_header : "Welkom op het dataportaal" }}
            </h1>
            <p v-if="config?.organization_introduction" class="tw-text-gray-600 tw-text-lg tw-leading-relaxed">
              {{ config.organization_introduction }}
            </p>
          </div>

          <!-- Right: Header Image -->
          <div
            v-if="config?.organization_image"
            class="tw-rounded-2xl tw-overflow-hidden tw-shadow-sm tw-flex tw-items-center"
          >
            <img
              :src="config.organization_image"
              class="tw-w-full tw-h-auto tw-max-h-[300px] md:tw-max-h-[400px] tw-object-cover"
              :alt="`Impressie van ${config?.organization_name}`"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <main class="tw-max-w-7xl tw-mx-auto tw-px-6 tw-py-16 tw-space-y-20">
      <Spinner v-if="loading" class="spinner" :style-type="'portal'" />
      <div v-else-if="hasCriticalError" class="tw-flex tw-justify-center tw-items-center tw-min-h-64">
        <div class="tw-text-center">
          <p class="tw-text-gray-600 tw-text-lg">
            Er is een probleem opgetreden bij het laden van de gegevens. Probeer het opnieuw.
          </p>
        </div>
      </div>
      <div v-else class="tw-space-y-20">
        <!-- Search and Quick Links Section -->
        <div class="tw-grid md:tw-grid-cols-3 tw-gap-8">
          <!-- Search Bar (2 columns on desktop) -->
          <div v-if="availableLinks.metadatasets" class="md:tw-col-span-2">
            <div class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-p-8">
              <h2 class="tw-text-2xl tw-mb-6">Zoeken</h2>
              <PortalSearchField @on-search="onSearch" />
            </div>
          </div>

          <!-- Direct naar links -->
          <div class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-p-8">
            <PortalQuickNavigationMenu :available-links="availableLinks" />
          </div>
        </div>

        <!-- Map Preview -->
        <section id="map">
          <div class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-overflow-hidden">
            <EmbedAtlasFrame :embed-url="embedUrl" />
          </div>
        </section>

        <div v-if="noContentAvailable" class="tw-flex tw-justify-center tw-text-xl">
          <p v-if="user">Het lijkt er op dat er nog geen data geconfigureerd is...</p>
        </div>
        <div v-else class="tw-space-y-20">
          <!-- Kaarten Section -->
          <section v-if="maps?.length || errors.maps" id="maps">
            <div class="tw-flex tw-items-center tw-justify-between tw-mb-8">
              <h2 class="tw-text-3xl">Kaarten</h2>
              <a
                v-if="maps?.length"
                href="/maps"
                class="tw-text-[var(--color-primary-organization)] hover:tw-opacity-80 tw-transition-colors tw-font-medium tw-text-lg tw-flex tw-items-center tw-gap-1 tw-no-underline"
              >
                Bekijk alle kaarten <i class="pi pi-arrow-right" aria-hidden="true"></i>
              </a>
            </div>
            <div v-if="errors.maps" class="tw-text-center tw-py-4">
              <p class="tw-text-red-600 tw-text-sm">{{ errors.maps }}</p>
            </div>
            <div class="tw-grid sm:tw-grid-cols-2 lg:tw-grid-cols-4 tw-gap-6">
              <PortalCard
                v-for="map in visibleMaps"
                :key="map.id"
                :object-type="'map'"
                :title="map.title"
                :thumbnail="map.thumbnail"
                :summary="map.description"
                :show-thumbnail="true"
                :object-url="`/atlas/maps/${map.slug}`"
              />
            </div>
          </section>

          <!-- Metadatasets Section -->
          <section v-if="metadatasets?.length || errors.metadatasets" id="metadata">
            <div class="tw-flex tw-items-center tw-justify-between tw-mb-8">
              <h2 class="tw-text-3xl">Metadatasets</h2>
              <a
                v-if="metadatasets?.length"
                href="/metadatasets"
                class="tw-text-[var(--color-primary-organization)] hover:tw-opacity-80 tw-transition-colors tw-font-medium tw-text-lg tw-flex tw-items-center tw-gap-1 tw-no-underline"
              >
                Bekijk alle metadatasets <i class="pi pi-arrow-right" aria-hidden="true"></i>
              </a>
            </div>
            <div v-if="errors.metadatasets" class="tw-text-center tw-py-4">
              <p class="tw-text-red-600 tw-text-sm">{{ errors.metadatasets }}</p>
            </div>
            <div class="tw-grid sm:tw-grid-cols-2 lg:tw-grid-cols-3 tw-gap-6">
              <PortalCard
                v-for="metadataset in visibleMetadatasets"
                :key="metadataset.id"
                :object-type="'metadataset'"
                :title="metadataset.title"
                :summary="metadataset.abstract || metadataset.description || ''"
                :thumbnail="metadataset.thumbnail"
                :show-thumbnail="false"
                :object-url="`/metadatasets/${metadataset.slug}`"
              />
            </div>
          </section>

          <!-- Tabellen Section -->
          <!-- Note: Tables are loaded from the store (not via API), so no error handling is needed -->
          <section v-if="tables?.length" id="tables">
            <div class="tw-flex tw-items-center tw-justify-between tw-mb-8">
              <h2 class="tw-text-3xl">Tabellen</h2>
              <a
                href="/tables"
                class="tw-text-[var(--color-primary-organization)] hover:tw-opacity-80 tw-transition-colors tw-font-medium tw-text-lg tw-flex tw-items-center tw-gap-1 tw-no-underline"
              >
                Bekijk alle tabellen <i class="pi pi-arrow-right" aria-hidden="true"></i>
              </a>
            </div>
            <div class="tw-grid sm:tw-grid-cols-2 lg:tw-grid-cols-3 tw-gap-6">
              <PortalCard
                v-for="table in visibleTables"
                :key="table.id"
                :object-type="'table'"
                :title="table.title"
                :summary="table.description"
                :thumbnail="table.thumbnail"
                :show-thumbnail="false"
                :object-url="`/tables/${table.slug}`"
              />
            </div>
          </section>
        </div>
      </div>
    </main>
  </div>
</template>

<script setup lang="ts">
import EmbedAtlasFrame from "@/components/EmbedAtlasFrame.vue";
import Spinner from "@/components/Spinner.vue";
import PortalCard from "@/portal/components/PortalCard.vue";
import PortalQuickNavigationMenu from "@/portal/components/PortalQuickNavigationMenu.vue";
import PortalSearchField from "@/portal/components/PortalSearchField.vue";
import { useGlobalStore } from "@/stores";
import { APIResponseType } from "@/types/APIResponseType";
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";

interface Map {
  id: number;
  title: string;
  description: string;
  thumbnail?: string;
  slug: string;
}

interface Metadataset {
  id: number;
  title: string;
  abstract?: string;
  description?: string;
  thumbnail?: string;
  slug: string;
}

interface Table {
  id: number;
  title: string;
  description: string;
  thumbnail?: string;
  slug: string;
}

interface AvailableLinks {
  maps: boolean;
  metadatasets: boolean;
  tables: boolean;
}

interface Config {
  organization_header?: string;
  organization_introduction?: string;
  organization_image?: string;
  organization_name?: string;
  position: {
    center: [number, number];
    zoom: number;
  };
}

const loading = ref(false);
const errors = ref({
  maps: null as string | null,
  metadatasets: null as string | null,
});
const metadatasets = ref<Metadataset[]>([]);
const maps = ref<Map[]>([]);
const maxNrItems = ref(4);
const embedUrl = ref("");

const router = useRouter();
const globalStore = useGlobalStore();

const user = computed(() => globalStore.user);
const config = computed<Config | null>(() => globalStore.config);
const tables = computed<Table[]>(() => globalStore.tables || []);

const visibleMaps = computed(() => maps.value.slice(0, maxNrItems.value));
const visibleMetadatasets = computed(() => metadatasets.value.slice(0, maxNrItems.value));
const visibleTables = computed(() => tables.value.slice(0, maxNrItems.value));

const noContentAvailable = computed(() => !maps.value?.length && !tables.value?.length && !metadatasets.value?.length);

const hasCriticalError = computed(() => errors.value.maps && errors.value.metadatasets);

const availableLinks = computed<AvailableLinks>(() => ({
  maps: maps.value?.length > 0,
  metadatasets: metadatasets.value?.length > 0,
  tables: tables.value?.length > 0,
}));

const getMetadatasets = async (): Promise<APIResponseType<Metadataset> | null> => {
  try {
    // For logged-in users, show all metadatasets regardless of status and show_in_overview
    // For anonymous users, only show completed metadatasets that are marked for overview
    const url = user.value
      ? "/atlas/api/v1/metadatasets/"
      : "/atlas/api/v1/metadatasets/?status=completed&show_in_overview=True";

    const result = await fetch(url, {
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
    });

    if (!result.ok) {
      console.error("Could not fetch metadatasets:", result.status, result.statusText);
      return null;
    }

    const response = await result.json();
    metadatasets.value = response.results || [];

    return response;
  } catch (error) {
    console.error("Error fetching metadatasets:", error);
    return null;
  }
};

const getMaps = async (): Promise<APIResponseType<Map> | null> => {
  try {
    const result = await fetch("/atlas/api/v1/maps/?published=True&show_in_overview=True", {
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
    });

    if (!result.ok) {
      console.error("Could not fetch maps:", result.status, result.statusText);
      return null;
    }

    const response = await result.json();
    maps.value = response.results || [];
    return response;
  } catch (error) {
    console.error("Error fetching maps:", error);
    return null;
  }
};

const onSearch = (searchQuery: string): void => {
  router.push(`/search/?query=${searchQuery}`);
};

const getEmbedUrl = (): string => {
  if (!config.value) {
    return "";
  }
  return `${encodeURI(window.location.origin)}/atlas/embed/@${encodeURIComponent(
    config.value.position.center[0],
  )},${encodeURIComponent(config.value.position.center[1])},${encodeURIComponent(Math.round(config.value.position.zoom * 100) / 100)}z/`;
};

const loadData = async (): Promise<void> => {
  loading.value = true;
  errors.value = {
    maps: null,
    metadatasets: null,
  };

  try {
    const [mapsResult, metadatasetsResult] = await Promise.all([getMaps(), getMetadatasets()]);

    // Set individual error messages for failed requests
    if (!mapsResult) {
      errors.value.maps = "Kon kaarten niet laden. Probeer het opnieuw.";
    }
    if (!metadatasetsResult) {
      errors.value.metadatasets = "Kon metadatasets niet laden. Probeer het opnieuw.";
    }
  } catch (err) {
    console.error("Unexpected error loading dashboard data:", err);
    errors.value.maps = "Er is een probleem opgetreden bij het laden van de gegevens.";
    errors.value.metadatasets = "Er is een probleem opgetreden bij het laden van de gegevens.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadData();
  embedUrl.value = getEmbedUrl();
});
</script>
