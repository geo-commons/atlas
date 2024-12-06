<template>
  <main class="tw-mx-auto tw-max-w-7xl tw-px-4 md:tw-pt-6 tw-my-4">
    <section class="tw-grid md:tw-grid-cols-12 lg:tw-gap-12 tw-gap-4">
      <div class="md:tw-col-span-7">
        <h1 class="tw-text-4xl tw-my-0 tw-mb-2">
          Dataportaal van de <span class="tw-lowercase">{{ config.organization_name }}!</span>
        </h1>
        <p v-if="config.organization_introduction" class="tw-leading-8">
          {{ config.organization_introduction }}
        </p>
      </div>
      <img
        v-if="config.organization_image"
        :src="config.organization_image"
        class="md:tw-col-span-5 tw-w-full tw-shadow"
        :alt="`Impressie van ${config.organization_name}`"
      />
    </section>
    <Spinner v-if="loading" class="spinner" :style-type="'portal'" />
    <div v-else class="tw-flex tw-flex-col tw-gap-4 md:tw-gap-8 tw-mt-4 md:tw-mt-8">
      <!-- Note: currently we can only search through datasets that is why it is the only check in the v-if below.     -->
      <section v-if="availableLinks.datasets" class="tw-flex tw-justify-center">
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
        <section v-if="maps?.length">
          <div class="tw-flex tw-justify-between tw-items-center">
            <h2 class="tw-text-4xl tw-mb-3 tw-mt-0">Kaarten</h2>
            <router-link class="text-button" to="/maps">
              Toon alle kaarten
              <ArrowRightIcon class="icon __smedium" />
            </router-link>
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
        <section v-if="datasets?.length">
          <div class="tw-flex tw-justify-between tw-items-center">
            <h2 class="tw-text-4xl tw-mb-3 tw-mt-0">Datasets</h2>
            <router-link class="text-button" to="/datasets">
              Toon alle datasets
              <ArrowRightIcon class="icon __smedium" />
            </router-link>
          </div>
          <div class="tw-grid sm:tw-grid-cols-2 md:tw-grid-cols-3 lg:tw-grid-cols-4 tw-gap-4 md:tw-gap-8">
            <PortalCard
              v-for="dataset in visibleDatasets"
              :key="dataset.id"
              :object-type="'dataset'"
              :title="dataset.title"
              :summary="dataset.description"
              :thumbnail="dataset.thumbnail"
              :show-thumbnail="true"
              :object-url="`/datasets/${dataset.slug}`"
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
              :object-url="`/tables/#/${table.slug}`"
            />
          </div>
        </section>
      </div>
    </div>
  </main>
</template>

<script>
import { useGlobalStore } from "@/stores";
import PortalCard from "@/portal/components/PortalCard.vue";
import PortalSearchField from "@/portal/components/PortalSearchField.vue";
import Spinner from "@/components/Spinner.vue";
import ArrowRightIcon from "../../assets/icons/arrow-right-icon.svg";
import PortalQuickNavigationMenu from "@/portal/components/PortalQuickNavigationMenu.vue";
import EmbedAtlasFrame from "@/components/EmbedAtlasFrame.vue";

export default {
  name: "PortalDashboard",
  components: { EmbedAtlasFrame, PortalQuickNavigationMenu, PortalSearchField, PortalCard, Spinner, ArrowRightIcon },
  data() {
    return {
      loading: false,
      datasets: [],
      maps: [],
      maxNrItems: 4,
      embedUrl: String,
    };
  },
  computed: {
    user() {
      return useGlobalStore().user;
    },
    config() {
      return useGlobalStore().config;
    },
    tables() {
      return useGlobalStore().tables ? useGlobalStore().tables : [];
    },
    visibleMaps() {
      return this.maps.slice(0, this.maxNrItems);
    },
    visibleDatasets() {
      return this.datasets.slice(0, this.maxNrItems);
    },
    visibleTables() {
      return this.tables.slice(0, this.maxNrItems);
    },
    noContentAvailable() {
      return !this.maps?.length && !this.tables?.length && !this.datasets?.length;
    },
    availableLinks() {
      return { maps: this.maps?.length > 0, datasets: this.datasets?.length > 0, tables: this.tables?.length > 0 };
    },
  },
  created() {
    Promise.all([this.getDatasets(), this.getMaps()]).then(() => {
      this.loading = false;
    });
    this.embedUrl = this.getEmbedUrl();
  },
  methods: {
    async getDatasets() {
      this.loading = true;

      const result = await fetch("/atlas/api/v1/datasets/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch datasets");
      }

      const response = await result.json();
      this.datasets = response.results;
      return result;
    },
    async getMaps() {
      this.loading = true;

      const result = await fetch("/atlas/api/v1/maps/", {
        credentials: "same-origin",
        headers: { "Content-Type": "application/json" },
      });

      if (!result.ok) {
        console.error("Could not fetch maps");
      }

      const response = await result.json();
      this.maps = response.results;
      return result;
    },
    onSearch(searchQuery) {
      this.$router.push(`/search/?query=${searchQuery}`);
    },
    getEmbedUrl() {
      return `${encodeURI(window.location.origin)}/atlas/embed/@${encodeURIComponent(
        this.config.position.center[0],
      )},${encodeURIComponent(this.config.position[1])},${encodeURIComponent(Math.round(this.config.position.zoom * 100) / 100)}z/`;
    },
  },
};
</script>
