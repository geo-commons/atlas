<template>
  <ExpandButton :title="computedTitle" :is-open="isOpen" class="feature">
    <template #default>
      <div>
        <span v-if="error">Er is een fout opgetreden tijdens het laden.</span>
        <span v-if="loading">Bezig met laden...</span>
        <span v-if="!loading && !error && displayProperties.length === 0">Geen weergave beschikbaar.</span>
        <div v-if="!loading && !error && displayProperties.length > 0">
          <table-list class="table">
            <table>
              <thead>
                <tr>
                  <th></th>
                  <th v-for="property in displayProperties" :key="property">
                    <SortableTableHeaderItem
                      :layer="layer"
                      :property="property"
                      :sort-key="sortKey"
                      :sort-ascending="sortAscending"
                      @sort="(column) => sortColumn(column)"
                    />
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="feature in sortedFeatures" :key="feature.id">
                  <td>
                    <button
                      v-if="feature.geometry"
                      v-tippy="{ placement: 'right' }"
                      class="iconbutton pin-button"
                      content="Bekijk op kaart"
                      aria-label="Bekijk op kaart"
                      @click="() => showFeature(feature)"
                    >
                      <svg
                        width="10px"
                        height="14px"
                        viewBox="0 0 10 14"
                        version="1.1"
                        xmlns="http://www.w3.org/2000/svg"
                        xmlns:xlink="http://www.w3.org/1999/xlink"
                      >
                        <g id="pin" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                          <path
                            id="Combined-Shape"
                            d="M5,0 C7.5155,0 9.55,2.0345 9.55,4.55 C9.55,7.9625 5,13 5,13 C5,13 0.45,7.9625 0.45,4.55 C0.45,2.0345 2.4845,0 5,0 Z M5,1.3 C3.206,1.3 1.75,2.756 1.75,4.55 C1.75,6.4025 3.648,9.2365 5,10.972 C6.378,9.2235 8.25,6.422 8.25,4.55 C8.25,2.756 6.794,1.3 5,1.3 Z M5,2.925 C5.89746272,2.925 6.625,3.65253728 6.625,4.55 C6.625,5.44746272 5.89746272,6.175 5,6.175 C4.10253728,6.175 3.375,5.44746272 3.375,4.55 C3.375,3.65253728 4.10253728,2.925 5,2.925 Z"
                            fill="#000000"
                            fill-rule="nonzero"
                          ></path>
                        </g>
                      </svg>
                    </button>
                  </td>
                  <td v-for="property in displayProperties" :key="property">
                    {{ feature.properties[property] }}
                  </td>
                </tr>
              </tbody>
            </table>
          </table-list>
        </div>
      </div>
    </template>
  </ExpandButton>
</template>

<script>
import GeoJSON from "ol/format/GeoJSON";
import { getCenter } from "ol/extent";

import TableList from "./TableList";
import ExpandButton from "./ExpandButton";
import SortableTableHeaderItem from "./SortableTableHeaderItem.vue";

export default {
  name: "FeatureTableExpandable",
  components: {
    ExpandButton,
    SortableTableHeaderItem,
    TableList,
  },
  props: {
    layer: Object,
    query: String,
    selectedArea: Object,
    isOpen: Boolean,
    isFilterable: Boolean,
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
      sortKey: "",
      sortAscending: true,
    };
  },
  computed: {
    computedTitle() {
      if (this.numberMatched !== null) {
        return `${this.layer.title} (${this.numberMatched})`;
      }

      return this.layer.title;
    },
    sortedFeatures() {
      if (this.sortKey && this.features) {
        return this.features.slice(0).sort((a, b) => {
          const textA = a.properties[this.sortKey];
          const textB = b.properties[this.sortKey];
          return this.sortAlphabetically(textA, textB, this.sortAscending);
        });
      }

      return this.features;
    },
  },
  watch: {
    query: "fetchFeatures",
    selectedArea: "fetchFeatures",
    filter: "fetchFeatures",
    fieldFilters: "fetchFeatures",
  },
  mounted() {
    this.fetchFeatures();
    this.fetchSearchProperties();
  },
  methods: {
    async fetchFeatures() {
      this.loading = true;
      this.error = false;

      const params = new URLSearchParams([
        ["service", "WFS"],
        ["version", "1.0.0"],
        ["request", "GetFeature"],
        ["typename", this.layer.name],
        ["outputFormat", "application/json"],
        ["maxFeatures", "5000"],
      ]);

      const filters = [];

      if (this.query && this.searchProperties.length > 0) {
        filters.push(this.searchProperties.map((key) => `${key} ILIKE '%${this.query}%'`).join(" OR "));
      }

      if (this.fieldFilters && Object.keys(this.fieldFilters).length > 0) {
        Object.keys(this.fieldFilters).forEach((key) => {
          filters.push(`${key} = '${this.fieldFilters[key]}'`);
        });
      }

      if (this.selectedArea) {
        filters.push(
          `INTERSECTS(geom,POLYGON((${this.selectedArea
            .getCoordinates()[0]
            .map((c) => `${c[0]} ${c[1]}`)
            .join(",")})))`
        );
      }

      if (filters.length > 0) {
        params.set("cql_filter", filters.join(" AND "));
      }

      if (this.overallFilter) {
        params.set("cql_filter", `${this.overallFilter.key} = '${this.overallFilter.value}'`);
      }

      try {
        const url = new URL(this.layer.url);
        url.search = params.toString();

        const result = await fetch(url.toString(), this.getFetchParameters());
        const data = await result.json();

        this.features = data.features;
        this.numberMatched = data.numberMatched;

        if (this.displayProperties.length === 0 && data.features.length > 0) {
          // cache first retrieval of properties into this.displayProperties
          const fetchedProperties = Object.keys(data.features[0].properties);

          this.displayProperties =
            this.layer.display_properties.length > 0 ? this.layer.display_properties : fetchedProperties;
        }
      } catch (e) {
        console.error(e);
        this.error = true;
        this.features = [];
        this.displayProperties = [];
        this.searchProperties = [];
        this.numberMatched = 0;
      }

      this.loading = false;
    },
    async fetchSearchProperties() {
      if (this.layer.search_properties && this.layer.search_properties.length > 0) {
        this.searchProperties = this.layer.search_properties;
        return;
      }

      const params = new URLSearchParams([
        ["service", "WFS"],
        ["version", "1.0.0"],
        ["request", "DescribeFeatureType"],
        ["typename", this.layer.name],
        ["outputFormat", "application/json"],
      ]);

      try {
        const url = new URL(this.layer.url);
        url.search = params.toString();

        const result = await fetch(url.toString(), this.getFetchParameters());

        const data = await result.json();
        const featureType = data.featureTypes[0];

        // Only search through properties with type string
        const stringProperties = featureType.properties.filter((p) => p.localType === "string");

        this.searchProperties = stringProperties.map((p) => p.name);
      } catch (e) {
        console.error(e);
      }
    },
    showFeature(feature) {
      const geometry = new GeoJSON().readFeature(feature).getGeometry();
      const center = getCenter(geometry.getExtent());

      this.$emit("set-position", {
        ...this.position,
        marker: center,
      });

      this.$emit("on-fit", geometry.getExtent());
    },
    getFetchParameters() {
      if (this.layer.source && this.layer.source.authenticate && this.user && this.user.token) {
        return {
          headers: { Authorization: `Bearer ${this.user.token}` },
        };
      }

      return {};
    },
    sortColumn(prop) {
      if (this.sortKey !== prop) {
        this.sortKey = prop;
        this.sortAscending = true;
      } else {
        this.sortAscending = !this.sortAscending;
      }
    },
    sortAlphabetically(a, b, ascending) {
      // equal items sort equally
      if (a === b) {
        return 0;
      }

      // nulls and empty strings sort after anything else
      if (a === null || a === "") {
        return 1;
      }
      if (b === null || b === "") {
        return -1;
      }

      // otherwise, if we're ascending, lowest sorts first
      if (ascending) {
        return a < b ? -1 : 1;
      }

      // if descending, highest sorts first
      return a < b ? 1 : -1;
    },
  },
};
</script>

<style scoped>
.feature:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-50);
}

.table {
  margin: 0 0 24px;
}

.iconbutton {
  width: var(--width-button-normal);
}

.pin-button {
  width: 100%;
  height: 26px;
}

td:first-child {
  width: var(--width-button-large);
  padding: 0 !important;
}

.table-header {
  display: flex;
}
</style>
