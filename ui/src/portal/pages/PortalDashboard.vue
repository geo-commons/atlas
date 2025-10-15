<template>
  <main class="tw-mx-auto tw-max-w-7xl tw-px-4 md:tw-pt-6 tw-my-4">
    <section class="tw-grid md:tw-grid-cols-12 lg:tw-gap-12 tw-gap-4">
      <div class="md:tw-col-span-7">
        <h1 class="tw-text-4xl tw-my-0 tw-mb-2">
          {{ config?.organization_header ? config.organization_header : "Welkom op het dataportaal!" }}
        </h1>
        <p v-if="config?.organization_introduction" class="tw-leading-8">
          {{ config.organization_introduction }}
        </p>
      </div>
      <img
        v-if="config?.organization_image"
        :src="config.organization_image"
        class="md:tw-col-span-5 tw-w-full tw-shadow"
        :alt="`Impressie van ${config?.organization_name}`"
      />
    </section>
    <Spinner v-if="loading" class="spinner" :style-type="'portal'" />
    <div v-else-if="hasCriticalError" class="tw-flex tw-justify-center tw-items-center tw-min-h-64">
      <div class="tw-text-center">
        <p class="tw-text-gray-600 tw-text-lg">
          Er is een probleem opgetreden bij het laden van de gegevens. Probeer het opnieuw.
        </p>
      </div>
    </div>
    <div v-else class="tw-flex tw-flex-col tw-gap-4 md:tw-gap-8 tw-mt-4 md:tw-mt-8">
      <!-- Note: currently we can only search through metadatasets that is why it is the only check in the v-if below.     -->
      <section v-if="availableLinks.metadatasets" class="tw-flex tw-justify-center">
        <div class="tw-w-full lg:tw-w-4/6">
          <PortalSearchField :size="'large'" @on-search="onSearch" />
        </div>
      </section>

      <section class="tw-grid md:tw-grid-cols-12 tw-gap-4 lg:tw-gap-12 tw-mt-4 md:tw-mt-8">
        <EmbedAtlasFrame class="md:tw-col-span-7" :embed-url="embedUrl" />
        <PortalQuickNavigationMenu :available-links="availableLinks" class="md:tw-col-span-5" />
      </section>

      <div v-if="noContentAvailable" class="tw-flex tw-justify-center tw-text-xl">
        <p v-if="user">Het lijkt er op dat er nog geen data geconfigureerd is...</p>
      </div>
      <div v-else class="tw-flex tw-flex-col tw-gap-4 md:tw-gap-8">
        <section v-if="maps?.length || errors.maps">
          <div class="tw-flex tw-justify-between tw-items-center">
            <h2 class="tw-text-4xl tw-mb-3 tw-mt-0">Kaarten</h2>
            <router-link v-if="maps?.length" class="text-button" to="/maps">
              Toon alle kaarten
              <ArrowRightIcon class="icon __smedium" />
            </router-link>
          </div>
          <div v-if="errors.maps" class="tw-text-center tw-py-4">
            <p class="tw-text-red-600 tw-text-sm">{{ errors.maps }}</p>
          </div>
          <div class="tw-grid sm:tw-grid-cols-2 md:tw-grid-cols-3 lg:tw-grid-cols-4 tw-gap-4 md:tw-gap-8">
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
        <section v-if="metadatasets?.length || errors.metadatasets">
          <div class="tw-flex tw-justify-between tw-items-center">
            <h2 class="tw-text-4xl tw-mb-3 tw-mt-0">Metadatasets</h2>
            <router-link v-if="metadatasets?.length" class="text-button" to="/metadatasets">
              Toon alle metadatasets
              <ArrowRightIcon class="icon __smedium" />
            </router-link>
          </div>
          <div v-if="errors.metadatasets" class="tw-text-center tw-py-4">
            <p class="tw-text-red-600 tw-text-sm">{{ errors.metadatasets }}</p>
          </div>
          <div class="tw-grid sm:tw-grid-cols-2 md:tw-grid-cols-3 lg:tw-grid-cols-4 tw-gap-4 md:tw-gap-8">
            <PortalCard
              v-for="metadataset in visibleMetadatasets"
              :key="metadataset.id"
              :object-type="'metadataset'"
              :title="metadataset.title"
              :summary="metadataset.description"
              :thumbnail="metadataset.thumbnail"
              :show-thumbnail="true"
              :object-url="`/metadatasets/${metadataset.slug}`"
            />
          </div>
        </section>
        <section v-if="tables?.length">
          <div class="tw-flex tw-justify-between tw-items-center">
            <h2 class="tw-text-4xl tw-mb-3 tw-mt-0">Tabellen</h2>
            <router-link class="text-button" to="/tables">
              Toon alle tabellen
              <ArrowRightIcon class="icon __smedium" />
            </router-link>
          </div>
          <div class="tw-grid sm:tw-grid-cols-2 md:tw-grid-cols-3 lg:tw-grid-cols-4 tw-gap-4 md:tw-gap-8">
            <PortalCard
              v-for="table in visibleTables"
              :key="table.id"
              :object-type="'table'"
              :title="table.title"
              :summary="table.description"
              :thumbnail="table.thumbnail"
              :show-thumbnail="true"
              :object-url="`/tables/${table.slug}`"
            />
          </div>
        </section>
      </div>
    </div>
  </main>
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
import ArrowRightIcon from "../../assets/icons/arrow-right-icon.svg";

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
  description: string;
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

  embedUrl.value = getEmbedUrl();
};

onMounted(() => {
  loadData();
});
</script>
