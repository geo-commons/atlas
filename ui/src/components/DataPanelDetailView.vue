<template>
  <div v-if="layer" class="detail-panel-wrapper">
    <div class="header">
      <div>
        <vue-tippy
          :arrow="false"
          placement="bottom-start"
          theme="popover"
          trigger="click"
          :distance="8"
          :delay="[0, 0]"
          :a11y="true"
        >
          <template #trigger>
            <button
              v-tippy="{ placement: 'right' }"
              class="iconbutton __normal __outline"
              content="Download"
              aria-label="Download"
            >
              <download-icon />
            </button>
          </template>
          <div class="container">
            <div class="menu">
              <ul class="list">
                <li>
                  <button @click="$refs.featureTable.downloadCSV()">
                    Download CSV
                  </button>
                </li>
                <li>
                  <button
                    @click="$refs.featureTable.download('ESRI Shapefile')"
                  >
                    Download ESRI Shape
                  </button>
                </li>
                <li>
                  <button @click="$refs.featureTable.download('GeoJSON')">
                    Download GeoJSON
                  </button>
                </li>
                <li>
                  <button @click="$refs.featureTable.download('GPKG')">
                    Download GeoPackage
                  </button>
                </li>
                <li>
                  <button @click="$refs.featureTable.download('GML')">
                    Download GML
                  </button>
                </li>
                <li>
                  <button @click="$refs.featureTable.download('SQLite')">
                    Download SQLite
                  </button>
                </li>
              </ul>
            </div>
          </div>
        </vue-tippy>
      </div>
      <SearchForm
        :show-border="true"
        :has-visible-layers="true"
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
          />
        </template>
      </SearchForm>
    </div>
    <FeatureTable
      ref="featureTable"
      :layer="layer"
      :position="position"
      :query="query"
      :selected-area="selectedArea"
      @set-position="(value) => onSetPosition(value)"
      @on-fit="(value) => onFit(value)"
    />
  </div>
</template>

<script>
import DownloadIcon from "../icons/DownloadIcon.vue";
import FeatureTable from "./FeatureTable.vue";
import SearchForm from "./SearchForm.vue";

export default {
  name: "DataPanelDetailView",
  components: { FeatureTable, SearchForm, DownloadIcon },
  props: {
    layer: Object,
    selectedArea: Object,
    isOpen: Boolean,
    overallFilter: Object,
    position: Object,
    user: Object,
  },
  data() {
    return {
      features: [],
      displayProperties: [],
      searchProperties: [],
      fieldFilters: {},
      loading: false,
      error: false,
      numberMatched: 0,
      query: "",
      sortKey: "",
      sortAscending: true,
    };
  },
  computed: {},
  mounted() {},
  methods: {
    onSetPosition(value) {
      this.$emit("set-position", value);
    },
    onFit(value) {
      this.$emit("on-fit", value);
    },
    onSearch() {
      this.query = this.$refs.queryInput.value;
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

@media (min-width: 576px) {
  .data-search {
    max-width: var(--width-detail);
  }
}
</style>
