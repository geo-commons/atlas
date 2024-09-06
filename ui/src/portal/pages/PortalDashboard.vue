<template>
  <main class="container __portal">
    <section class="intro-section">
      <div class="intro-text">
        <h1>
          Dataportaal van de <span class="lower">{{ config.organization_name }}!</span>
        </h1>
        <p v-if="config.organization_introduction" class="introduction">
          {{ config.organization_introduction }}
        </p>
      </div>
      <img
        v-if="config.organization_image"
        :src="config.organization_image"
        class="impressie"
        :alt="`Impressie van ${config.organization_name}`"
      />
    </section>
    <Spinner v-if="loading" class="spinner" :style-type="'portal'" />
    <div v-else-if="noContentAvailable" class="no-data-wrapper">
      <p>Het lijkt er op dat er nog geen data geconfigureerd is...</p>
    </div>
    <div v-else class="portal-dashboard-content">
      <section class="flex __center">
        <div class="search-container">
          <PortalSearchField :size="'large'" @on-search="onSearch" />
        </div>
      </section>

      <section v-if="maps.length">
        <div class="section-header">
          <h2>Kaarten</h2>
          <router-link class="text-button" to="/maps">
            Toon alle kaarten
            <ArrowRightIcon class="icon __smedium" />
          </router-link>
        </div>
        <div class="card-container">
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

      <section v-if="datasets.length">
        <div class="section-header">
          <h2>Datasets</h2>
          <router-link class="text-button" to="/datasets">
            Toon alle datasets
            <ArrowRightIcon class="icon __smedium" />
          </router-link>
        </div>
        <div class="card-container">
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
      <section v-if="tables.length">
        <div class="section-header">
          <h2>Tabellen</h2>
          <router-link class="text-button" to="/tables">
            Toon alle tabellen
            <ArrowRightIcon class="icon __smedium" />
          </router-link>
        </div>
        <div class="card-container">
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
  </main>
</template>

<script>
import { useGlobalStore } from "@/stores";
import PortalCard from "@/portal/components/PortalCard.vue";
import PortalSearchField from "@/portal/components/PortalSearchField.vue";
import Spinner from "@/components/Spinner.vue";
import ArrowRightIcon from "../../assets/icons/arrow-right-icon.svg";

export default {
  name: "PortalDashboard",
  components: { PortalSearchField, PortalCard, Spinner, ArrowRightIcon },
  data() {
    return {
      loading: false,
      datasets: [],
      maps: [],
      maxNrItems: 4,
    };
  },
  computed: {
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
      return !this.maps.length && !this.tables.length && !this.datasets.length;
    },
  },
  created() {
    Promise.all([this.getDatasets(), this.getMaps()]).then(() => {
      this.loading = false;
    });
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

      this.datasets = await result.json();
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

      this.maps = await result.json();
      return result;
    },
    onSearch(searchQuery) {
      this.$router.push(`/search/?query=${searchQuery}`);
    },
  },
};
</script>

<style scoped>
.lower {
  text-transform: lowercase;
}

.intro-section {
  display: grid;
  grid-template-columns: 1fr;
  margin-top: 20px;
}

@media (min-width: 1024px) {
  .intro-section {
    display: grid;
    grid-template-columns: 7fr 5fr;
    column-gap: 40px;
    margin-top: 40px;
  }
}

.intro-text {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.section-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.introduction {
  margin: 0;
  line-height: 1.9;
  font-size: var(--font-size-normal);
}

h1 {
  font-size: var(--font-size-2xl);
  margin: 0;
  line-height: 1.2;
}

h2 {
  font-size: var(--font-size-2xl);
  margin: 12px 0;
}

@media (min-width: 1024px) {
  h2 {
    font-size: var(--font-size-3xl);
    margin: 20px 0;
  }
}

.search-container {
  padding-top: 40px;
  width: 100%;
}

@media (min-width: 1024px) {
  .search-container {
    padding-top: 60px;
    width: 70%;
  }
}

.impressie {
  width: 100%;
  height: auto;
  box-shadow: var(--shadow-light);
}

.portal-dashboard-content {
  display: flex;
  flex-direction: column;
  gap: 32px;
}

.no-data-wrapper {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 40%;
  font-size: var(--font-size-xl);
}
</style>
