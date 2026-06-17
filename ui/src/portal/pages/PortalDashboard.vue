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
            <p
              v-if="config?.organization_introduction"
              class="tw-text-[var(--color-text-organization)] tw-text-lg tw-leading-relaxed"
            >
              {{ config.organization_introduction }}
            </p>
          </div>

          <!-- Right: Header Image -->
          <div
            v-if="config?.organization_image"
            class="tw-rounded-2xl tw-overflow-hidden tw-shadow-sm tw-flex tw-items-center tw-max-h-[300px] md:tw-max-h-[400px]"
          >
            <img
              :src="config.organization_image"
              class="tw-object-cover tw-w-full tw-h-full"
              :alt="`Impressie van ${config?.organization_name}`"
            />
          </div>
        </div>
      </div>
    </section>

    <!-- Main Content -->
    <main id="main-content" class="tw-max-w-7xl tw-mx-auto tw-px-6 tw-py-16 tw-space-y-20">
      <Spinner v-if="loading" class="spinner" :style-type="'portal'" />
      <div v-else-if="hasCriticalError" class="tw-flex tw-justify-center tw-items-center tw-min-h-64">
        <div class="tw-text-center">
          <p class="tw-text-[var(--color-text-organization)] tw-text-lg">
            Er is een probleem opgetreden bij het laden van de gegevens. Probeer het opnieuw.
          </p>
        </div>
      </div>
      <div v-else class="tw-space-y-20">
        <!-- Search and Quick Links Section -->
        <div class="tw-grid md:tw-grid-cols-3 tw-gap-8">
          <!-- Search Bar (2 columns on desktop) -->
          <div
            v-if="availableLinks.metadatasets || availableLinks.maps || availableLinks.tables"
            class="md:tw-col-span-2"
          >
            <div class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-p-8">
              <h2 class="tw-text-2xl tw-mb-6 tw-mt-2">Zoeken</h2>
              <PortalSearchField @on-search="onSearch" />
            </div>
          </div>

          <!-- Direct naar links -->
          <div class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-p-8">
            <PortalQuickNavigationMenu />
          </div>
        </div>

        <!-- Map Preview -->
        <section id="map">
          <div class="tw-bg-white tw-rounded-2xl tw-border tw-border-gray-200 tw-shadow-sm tw-overflow-hidden">
            <EmbedAtlasFrame :embed-url="embedUrl" />
          </div>
        </section>

        <div
          v-if="noContentAvailable"
          class="tw-flex tw-justify-center tw-text-xl tw-text-[var(--color-text-organization)]"
        >
          <p v-if="user">Het lijkt er op dat er nog geen data geconfigureerd is...</p>
        </div>
        <div v-else class="tw-space-y-20">
          <!-- Kaarten Section -->
          <section v-if="maps?.length || errors.maps" id="maps">
            <div class="tw-flex tw-items-baseline tw-justify-between tw-mb-8 tw-flex-wrap">
              <h2 class="tw-text-3xl">Kaarten</h2>
              <a
                v-if="maps?.length"
                href="/maps"
                class="tw-text-[var(--color-primary-organization)] hover:tw-opacity-80 tw-transition-colors tw-font-medium tw-text-lg tw-flex tw-items-center tw-gap-1 tw-no-underline focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-[var(--color-primary-organization)] focus-visible:tw-ring-offset-2"
              >
                Bekijk alle kaarten <i class="pi pi-arrow-right" aria-hidden="true"></i>
              </a>
            </div>
            <div v-if="errors.maps" class="tw-text-center tw-py-4">
              <p class="tw-text-red-600 tw-text-sm">{{ errors.maps }}</p>
            </div>
            <div class="tw-grid sm:tw-grid-cols-2 lg:tw-grid-cols-3 tw-gap-6">
              <PortalCard
                v-for="map in visibleMaps"
                :key="map.id"
                :object-type="PortalCardObjectType.Map"
                :title="map.title"
                :thumbnail="map.thumbnail ?? null"
                :summary="map.description"
                :show-thumbnail="true"
                :object-url="`/atlas/maps/${map.slug}`"
                :last-updated="null"
                :category="null"
              />
            </div>
          </section>

          <!-- Metadatasets Section -->
          <section v-if="metadatasets?.length || errors.metadatasets" id="metadata">
            <div class="tw-flex tw-items-baseline tw-justify-between tw-mb-8 tw-flex-wrap">
              <h2 class="tw-text-3xl">Metadatasets</h2>
              <a
                v-if="metadatasets?.length"
                href="/metadatasets"
                class="tw-text-[var(--color-primary-organization)] hover:tw-opacity-80 tw-transition-colors tw-font-medium tw-text-lg tw-flex tw-items-center tw-gap-1 tw-no-underline focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-[var(--color-primary-organization)] focus-visible:tw-ring-offset-2"
              >
                Bekijk alle metadatasets <i class="pi pi-arrow-right" aria-hidden="true"></i>
              </a>
            </div>
            <div v-if="errors.metadatasets" class="tw-text-center tw-py-4">
              <p class="tw-text-red-600 tw-text-sm">{{ errors.metadatasets }}</p>
            </div>
            <div class="tw-grid sm:tw-grid-cols-2 lg:tw-grid-cols-3 tw-gap-6">
              <div v-for="metadataset in visibleMetadatasets" :key="metadataset.id" class="tw-relative">
                <PortalCard
                  :object-type="PortalCardObjectType.Metadataset"
                  :title="metadataset.title"
                  :summary="metadataset.abstract || metadataset.description || ''"
                  :thumbnail="metadataset.thumbnail ?? null"
                  :show-thumbnail="false"
                  :object-url="`/metadatasets/${metadataset.slug}`"
                  :last-updated="metadataset.last_updated ?? null"
                  :category="null"
                />
                <span v-if="isInternalMetadataset(metadataset) && user" class="tw-absolute tw-top-3 tw-right-3 tw-z-10">
                  <VisibilityIndicator visibility="Intern" />
                </span>
              </div>
            </div>
          </section>

          <!-- Tabellen Section -->
          <section v-if="tables?.length || errors.tables" id="tables">
            <div class="tw-flex tw-items-baseline tw-justify-between tw-mb-8 tw-flex-wrap">
              <h2 class="tw-text-3xl">Tabellen</h2>
              <a
                v-if="tables?.length"
                href="/tables"
                class="tw-text-[var(--color-primary-organization)] hover:tw-opacity-80 tw-transition-colors tw-font-medium tw-text-lg tw-flex tw-items-center tw-gap-1 tw-no-underline focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-[var(--color-primary-organization)] focus-visible:tw-ring-offset-2"
              >
                Bekijk alle tabellen <i class="pi pi-arrow-right" aria-hidden="true"></i>
              </a>
            </div>
            <div v-if="errors.tables" class="tw-text-center tw-py-4">
              <p class="tw-text-red-600 tw-text-sm">{{ errors.tables }}</p>
            </div>
            <div v-else class="tw-grid sm:tw-grid-cols-2 lg:tw-grid-cols-3 tw-gap-6">
              <div v-for="table in visibleTables" :key="table.id" class="tw-relative">
                <PortalCard
                  :object-type="PortalCardObjectType.Table"
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
import VisibilityIndicator from "@/components/VisibilityIndicator.vue";
import { PortalCardObjectType } from "@/portal/components/shared/portalCardShared";
import { useGlobalStore, type PortalAvailableLinks } from "@/stores";
import { APIResponseType } from "@/types/APIResponseType";
import { computed, onMounted, ref } from "vue";
import { useRouter } from "@/utils/inertia-routing";
import { IRelatedTable } from "@/types/related-table";

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
  last_updated?: string | null;
  authorization_level?: string;
  show_in_overview?: boolean;
}

interface Config {
  organization_header?: string;
  organization_introduction?: string;
  organization_image?: string;
  organization_name?: string;
  organization_title_color?: string;
  organization_text_color?: string;
  position: {
    center: {
      x: number;
      y: number;
    };
    zoom: number;
  };
}

const loading = ref(false);
const errors = ref({
  maps: null as string | null,
  metadatasets: null as string | null,
  tables: null as string | null,
});
const metadatasets = ref<Metadataset[]>([]);
const maps = ref<Map[]>([]);
const tables = ref<IRelatedTable[]>([]);
const maxNrItems = ref(4);
const embedUrl = ref("");

const router = useRouter();
const globalStore = useGlobalStore();

const user = computed(() => globalStore.user);
const config = computed<Config | null>(() => globalStore.config);

const visibleMaps = computed(() => maps.value.slice(0, maxNrItems.value));
const visibleMetadatasets = computed(() => metadatasets.value.slice(0, maxNrItems.value));
const visibleTables = computed(() => tables.value.slice(0, maxNrItems.value));

const noContentAvailable = computed(() => !maps.value?.length && !tables.value?.length && !metadatasets.value?.length);

const hasCriticalError = computed(() => errors.value.maps && errors.value.metadatasets);

// portalAvailableLinks comes from server-rendered initial context (portal/views.py).
const availableLinks = computed<PortalAvailableLinks>(() => globalStore.portalAvailableLinks);

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
      return null;
    }

    const response = await result.json();
    metadatasets.value = response.results || [];

    return response;
  } catch {
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
      return null;
    }

    const response = await result.json();
    maps.value = response.results || [];
    return response;
  } catch {
    return null;
  }
};

const getTables = async (): Promise<APIResponseType<IRelatedTable> | null> => {
  try {
    const result = await fetch("/atlas/api/v1/tables/?page_size=12&show_in_portal=True", {
      credentials: "same-origin",
      headers: { "Content-Type": "application/json" },
    });

    if (!result.ok) {
      tables.value = [];
      return null;
    }

    const response = await result.json();
    tables.value = response.results || [];
    return response;
  } catch {
    tables.value = [];
    return null;
  }
};

const isInternalMetadataset = (metadataset: Metadataset): boolean => {
  return metadataset.authorization_level === "internal" || !metadataset.show_in_overview;
};

const onSearch = (searchQuery: string): void => {
  router.push(`/search/?query=${searchQuery}`);
};

const getEmbedUrl = (): string => {
  if (!config.value) {
    return "";
  }

  return `${encodeURI(window.location.origin)}/atlas/@${encodeURIComponent(
    config.value.position.center.x,
  )},${encodeURIComponent(config.value.position.center.y)},${encodeURIComponent(Math.round(config.value.position.zoom * 100) / 100)}z/.../.../is_embed=true`;
};

const loadData = async (): Promise<void> => {
  loading.value = true;
  errors.value = {
    maps: null,
    metadatasets: null,
    tables: null,
  };

  try {
    const [mapsResult, metadatasetsResult, tablesResult] = await Promise.all([
      getMaps(),
      getMetadatasets(),
      getTables(),
    ]);

    if (!mapsResult) {
      errors.value.maps = "Kon kaarten niet laden. Probeer het opnieuw.";
    }
    if (!metadatasetsResult) {
      errors.value.metadatasets = "Kon metadatasets niet laden. Probeer het opnieuw.";
    }
    if (!tablesResult) {
      errors.value.tables = "Kon tabellen niet laden. Probeer het opnieuw.";
    }
  } catch {
    errors.value.maps = "Er is een probleem opgetreden bij het laden van de gegevens.";
    errors.value.metadatasets = "Er is een probleem opgetreden bij het laden van de gegevens.";
    errors.value.tables = "Er is een probleem opgetreden bij het laden van de gegevens.";
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  loadData();
  embedUrl.value = getEmbedUrl();
});
</script>
