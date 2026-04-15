<template>
  <div v-if="layer" class="detail-panel-wrapper">
    <div class="header">
      <div>
        <tippy
          ref="downloadMenu"
          :arrow="false"
          placement="bottom-start"
          theme="popover"
          trigger="click"
          :distance="8"
          :delay="[0, 0]"
          :a11y="true"
          :interactive="true"
        >
          <button
            v-if="layer.is_exportable"
            v-tippy="{ placement: 'right' }"
            :disabled="isDownloadPending"
            class="iconbutton __normal __outline"
            content="Download"
            aria-label="Download"
          >
            <DownloadIcon v-if="!isDownloadPending" />
            <ProgressSpinner
              v-else
              stroke-width="4"
              fill="transparent"
              :pt="{ root: '!tw-max-w-6 !tw-max-h-6', circle: '!tw-stroke-black' }"
            />
          </button>
          <template #content>
            <div class="menu">
              <ul class="list">
                <li>
                  <button :disabled="isDownloadPending" @click="$refs.featureTable.download('CSV')">
                    Download CSV
                  </button>
                </li>
                <li>
                  <button :disabled="isDownloadPending" @click="$refs.featureTable.download('ESRI Shapefile')">
                    Download ESRI Shape
                  </button>
                </li>
                <li>
                  <button :disabled="isDownloadPending" @click="$refs.featureTable.download('GeoJSON')">
                    Download GeoJSON
                  </button>
                </li>
                <li>
                  <button :disabled="isDownloadPending" @click="$refs.featureTable.download('GPKG')">
                    Download GeoPackage
                  </button>
                </li>
                <li>
                  <button :disabled="isDownloadPending" @click="$refs.featureTable.download('GML')">
                    Download GML
                  </button>
                </li>
                <!-- TODO: Add download for SQLite, currently not supported by GeoServer -->
                <!-- <li>
                  <button :disabled="isDownloadPending" @click="$refs.featureTable.download('SQLite')">
                    Download SQLite
                  </button>
                </li> -->
              </ul>
            </div>
          </template>
        </tippy>
      </div>
      <SearchForm
        :show-border="true"
        :has-visible-layers="true"
        :disable-data-panel-button="true"
        class="data-search"
        @on-submit="onSearch"
      >
        <template #default>
          <input
            ref="queryInput"
            type="search"
            name="search"
            placeholder="Zoek data"
            autocomplete="off"
            class="search-address"
          />
        </template>
      </SearchForm>
    </div>
    <FeatureTable
      ref="featureTable"
      :layer="layer"
      :position="position"
      :search-value="searchValue"
      :map-id="mapId"
      :selected-area="selectedArea"
      :user="user"
      @download-pending="onDownloadPending"
      @show-feature-on-map="showFeatureOnMap"
    />
  </div>
</template>

<script>
import DownloadIcon from "../assets/icons/download-icon.svg";
import FeatureTable from "./FeatureTable.vue";
import SearchForm from "./SearchForm.vue";
import { Tippy } from "vue-tippy";
import { useMapStore } from "@/stores/map_store";

export default {
  name: "DataPanelDetailView",
  components: { Tippy, FeatureTable, SearchForm, DownloadIcon },
  props: {
    layer: Object,
    mapId: String,
    selectedArea: Object,
    isOpen: Boolean,
    position: Object,
    user: Object,
  },
  emits: ["show-feature-on-map"],
  data() {
    return {
      features: [],
      displayProperties: [],
      searchProperties: [],
      loading: false,
      store: null,
      searchValue: "",
      error: false,
      numberMatched: 0,
      sortKey: "",
      sortAscending: true,
      isDownloadPending: false,
    };
  },
  created() {
    this.store = useMapStore(this.mapId);
  },
  mounted() {
    const value = this.store.getSearchValueForLayer(this.layer.id);
    this.searchValue = value;

    this.$refs.queryInput.value = value;
  },
  methods: {
    onDownloadPending(isPending) {
      this.isDownloadPending = isPending;
      if (isPending) {
        // Close the menu when download starts
        this.$refs.downloadMenu?.hide?.();
      }
    },
    showFeatureOnMap(feature) {
      this.$emit("show-feature-on-map", feature);
    },
    onSearch() {
      this.searchValue = this.$refs.queryInput.value;
    },
  },
};
</script>

<style scoped>
.detail-panel-wrapper {
  padding: 0 var(--padding-screen);
  display: flex;
  flex-direction: column;
  height: 100%;
}

.header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  gap: 25px;
  padding-bottom: 18px;
}

.search-address {
  width: 100%;
  padding-left: 16px;
}

@media (min-width: 576px) {
  .data-search {
    max-width: var(--width-detail);
  }
}
</style>
