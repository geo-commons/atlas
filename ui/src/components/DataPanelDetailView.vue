<template>
  <div v-if="layer" class="detail-panel-wrapper">
    <div class="header">
      <div class="sticky-btn">
        <button
          v-tippy="{ placement: 'right' }"
          class="iconbutton __normal __outline sticky-btn"
          content="Download CSV"
          aria-label="Download CSV"
          @click="downloadCSV"
        >
          <download-icon />
        </button>
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
    downloadCSV() {
      const separator = ";";
      const filename = this.layer.title
        .replace(" ", "-")
        .replace(/[^a-z0-9-]/gi, "")
        .toLowerCase();

      let data =
        this.displayProperties
          .map((property) => `"${property.replace(/"/g, '""')}"`)
          .join(separator) + "\n";

      this.features.forEach((feature) => {
        data +=
          this.displayProperties
            .map((property) =>
              feature.properties[property] !== null
                ? `"${String(feature.properties[property]).replace(
                    /"/g,
                    '""'
                  )}"`
                : ""
            )
            .join(separator) + "\n";
      });

      const hiddenElement = document.createElement("a");
      hiddenElement.href =
        "data:text/csv;charset=utf-8," + encodeURIComponent(data);
      hiddenElement.target = "_blank";
      hiddenElement.download = `${filename}.csv`;
      hiddenElement.click();
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
  justify-content: flex-end;
  gap: 25px;
  padding-bottom: 18px;
}

.sticky-btn {
  margin: auto 0;
}

@media screen and (min-width: 800px) {
  .sticky-btn {
    width: 100%;
  }
}

@media (min-width: 576px) {
  .data-search {
    max-width: var(--width-detail);
  }
}
</style>
