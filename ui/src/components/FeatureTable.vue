<template>
  <div class="filter-table-container">
    <div class="filter-container">
      <div class="toggle-filter-container">
        <switch-slider aria-label="Activeer filters" @toggleSwitch="toggleFilters()" />
        <div>Activeer filters</div>
      </div>
      <div v-if="showFilters" class="filter-padding filter-grid">
        <div>
          <label for="selected_columns" class="filter-label-padding">Kolom(men) om op te filteren</label>
          <multiselect
            id="selected_columns"
            v-model="selectedFilterProperties"
            :options="filterProperties"
            :multiple="true"
            :show-labels="false"
            :placeholder="'Kies kolom(men)'"
            open-direction="bottom"
            @remove="(filter) => removeFilter(filter)"
          />
        </div>
        <div v-if="selectedFilterProperties" class="selected-filter-container">
          <div v-for="property in selectedFilterProperties" :key="property">
            <FilterSelect
              :filter-options="getFilterOptions(property)"
              :field-filters="fieldFilters"
              :filter-property="property"
              @onFilterChange="(v) => setFieldFilters(v, property)"
            />
          </div>
        </div>
      </div>
    </div>

    <p v-if="numberMatched !== null" class="total-results">
      {{ numberMatched }} {{ numberMatched === 1 ? "resultaat" : "resultaten" }}
    </p>

    <table-list v-if="!loading" class="table table-border table-margin">
      <table>
        <thead>
          <tr>
            <th></th>
            <th v-for="property in displayProperties" :key="property">
              <StackSortableTableHeaderItem
                :header-text="headerText(property)"
                :property="property"
                :sort-stack="sortStack"
                @sort="(column, ascending) => sortColumn(column, ascending)"
              />
            </th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="feature in featureCollection.features" :key="feature.id">
            <td>
              <button
                v-if="feature.geometry"
                v-tippy="{ placement: 'right' }"
                class="iconbutton __small __round"
                content="Bekijk op kaart"
                aria-label="Bekijk op kaart"
                @click="() => showFeature(feature)"
              >
                <MarkerIcon class="icon __small" />
              </button>
            </td>
            <td v-for="property in displayProperties" :key="property">
              {{ feature.properties[property] }}
            </td>
          </tr>
        </tbody>
      </table>
    </table-list>
    <Spinner v-else />
  </div>
</template>

<script>
import Cookies from "js-cookie";
import TableList from "./TableList.vue";
import GeoJSON from "ol/format/GeoJSON";
import { getFeatureCenterCoordinates } from "@/utils/geometry-helpers";
import Multiselect from "vue-multiselect";
import FilterSelect from "./FilterSelect.vue";
import SwitchSlider from "./SwitchSlider.vue";
import Spinner from "@/components/Spinner.vue";
import MarkerIcon from "../assets/icons/marker-icon.svg";
import { getFetchParameters } from "../utils/auth";
import StackSortableTableHeaderItem from "@/components/StackSortableTableHeaderItem.vue";

export default {
  name: "FeatureTable",
  components: {
    StackSortableTableHeaderItem,
    TableList,
    MarkerIcon,
    FilterSelect,
    Multiselect,
    SwitchSlider,
    Spinner,
  },
  props: {
    layer: Object,
    position: Object,
    query: String,
    selectedArea: Object,
    user: Object,
  },
  data() {
    return {
      featureCollection: {
        features: [],
      },
      displayProperties: [],
      fieldFilters: {},
      selectedFilterProperties: [],
      showFilters: false,
      filters: {},
      filterProperties: [],
      filterOptions: {},
      filterFeatures: {},
      loading: false,
      numberMatched: null,
      sortStack: [],
    };
  },
  watch: {
    query() {
      this.fetchFeatures();

      // If query gets deleted or removed, set searchValue to an empty string
      if (!this.query) {
        this.$emit(
          "update-filters",
          {
            ...this.filters,
            [this.layer.id]: {
              ...this.fieldFilters,
              search: "",
            },
          },
          this.layer.id,
        );
      }
    },
    selectedArea: "fetchFeatures",
    filter: "fetchFeatures",
    fieldFilters: "fetchFeatures",
    sortStack() {
      this.fetchFeatures();
    },
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
        const searchQuery = `(${this.searchProperties.map((key) => `${key} ILIKE '%${this.query}%'`).join(" OR ")})`;

        filters.push(searchQuery);

        this.$emit(
          "update-filters",
          {
            ...this.filters,
            [this.layer.id]: {
              ...this.fieldFilters,
              search: searchQuery,
            },
          },
          this.layer.id,
        );
      }

      if (this.fieldFilters && Object.keys(this.fieldFilters).length > 0) {
        Object.keys(this.fieldFilters).forEach((key) => {
          filters.push(`${key} in (${this.fieldFilters[key].map((f) => this.replaceQuotes(f)).join(",")})`);
        });
      }

      if (this.selectedArea) {
        filters.push(
          `INTERSECTS(geom,POLYGON((${this.selectedArea
            .getCoordinates()[0]
            .map((c) => `${c[0]} ${c[1]}`)
            .join(",")})))`,
        );
      }

      if (filters.length > 0) {
        params.set("cql_filter", filters.join(" AND "));
      }

      if (this.sortStack.length > 0) {
        let sortString = [];

        this.sortStack.map((attr) => {
          sortString.push(`${attr.id} ${attr.asc ? "A" : "D"}`);
        });

        params.set("sortBy", sortString);
      }

      try {
        const url = new URL(this.layer.url);
        url.search = params.toString();

        const result = await fetch(url.toString(), getFetchParameters(this.layer, this.user));
        const data = await result.json();

        this.featureCollection = data;

        this.numberMatched = data.numberMatched;

        if (this.displayProperties.length === 0 && data.features.length > 0) {
          // cache first retrieval of properties into this.displayProperties
          const fetchedProperties = Object.keys(data.features[0].properties);

          this.displayProperties =
            this.layer.display_properties.length > 0 ? this.layer.display_properties : fetchedProperties;

          // Remove empty columns from the filter options.
          let emptyColumn = this.displayProperties.slice(0);

          data.features.forEach((feature) => {
            emptyColumn.forEach((prop) => {
              if (feature.properties[prop] && feature.properties[prop] !== "") {
                // Remove a column from the empty column array as soon as a corresponding cell is found that
                // contains a value.
                emptyColumn.splice(emptyColumn.indexOf(prop), 1);
              }
            });
          });

          this.filterProperties = this.displayProperties.filter((prop) => !emptyColumn.includes(prop));
        }
      } catch (e) {
        console.error(e);
        this.error = true;
        this.featureCollection = { features: [] };
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

        const result = await fetch(url.toString(), getFetchParameters(this.layer, this.user));

        const data = await result.json();
        const featureType = data.featureTypes[0];

        // Only search through properties with type string
        const stringProperties = featureType.properties.filter((p) => p.localType === "string");

        this.searchProperties = stringProperties.map((p) => p.name);
      } catch (e) {
        console.error(e);
      }
    },
    downloadCSV() {
      const separator = ";";
      const filename = this.layer.title
        .replace(" ", "-")
        .replace(/[^a-z0-9-]/gi, "")
        .toLowerCase();

      let data = this.displayProperties.map((property) => `"${property.replace(/"/g, '""')}"`).join(separator) + "\n";

      this.featureCollection.features.forEach((feature) => {
        data +=
          this.displayProperties
            .map((property) =>
              feature.properties[property] !== null
                ? `"${String(feature.properties[property]).replace(/"/g, '""')}"`
                : "",
            )
            .join(separator) + "\n";
      });

      const hiddenElement = document.createElement("a");
      hiddenElement.href = "data:text/csv;charset=utf-8," + encodeURIComponent(data);
      hiddenElement.target = "_blank";
      hiddenElement.download = `${filename}.csv`;
      hiddenElement.click();
    },
    async download(outputFormat) {
      const result = await fetch(`/atlas/convert/${outputFormat}`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: JSON.stringify({
          outputFormat,
          featureCollection: this.featureCollection,
        }),
      });

      const formats = {
        "ESRI Shapefile": ".shp.zip",
        GeoJSON: ".geojson",
        GPKG: ".gpkg",
        GML: ".gml",
        SQLite: ".sqlite3",
      };

      const filename = this.layer.title
        .replace(" ", "-")
        .replace(/[^a-z0-9-]/gi, "")
        .toLowerCase();

      const data = await result.blob();
      const url = window.URL.createObjectURL(data);
      const a = document.createElement("a");
      a.href = url;
      a.download = `${filename}${formats[outputFormat]}`;
      document.body.appendChild(a);
      a.click();
      a.remove();
    },
    replaceQuotes(value) {
      if (typeof value === "string") {
        return `'${value.replace(/'/g, "''")}'`;
      } else {
        return value;
      }
    },
    showFeature(feature) {
      const geometry = new GeoJSON().readFeature(feature).getGeometry();
      const center = getFeatureCenterCoordinates(feature);

      this.$emit("set-position", {
        ...this.position,
        marker: center,
      });

      this.$emit("on-fit", geometry.getExtent());
    },
    sortColumn(column, ascending) {
      const index = this.sortStack.findIndex((item) => item.id === column);

      if (ascending !== null) {
        // If ascending is not null, either add or update the sortStack
        if (index === -1) {
          // If column doesn't exist, add it
          this.sortStack.push({ id: column, asc: ascending });
        } else {
          // If column exists, update it if necessary
          if (this.sortStack[index].asc !== ascending) {
            this.sortStack[index].asc = ascending;
          }
        }
      } else {
        // If ascending is null, remove the column from sortStack if it exists
        if (index !== -1) {
          this.sortStack.splice(index, 1);
        }
      }
    },
    getFilterOptions(property) {
      if (this.filterOptions[property]) {
        return this.filterOptions[property];
      }

      // initialize filters for relevant feature property
      let filters = [];
      let featurePropSet = new Set();

      if (this.filterFeatures && property) {
        this.filterFeatures.forEach((feature) => {
          if (feature.properties[property]) {
            featurePropSet.add(feature.properties[property]);
          }
        });
      }
      filters = [...featurePropSet];
      this.filterOptions[property] = filters;
      return this.filterOptions[property];
    },
    setFieldFilters(v) {
      let newFilters = { ...this.filters };

      newFilters[this.layer.id] = {
        ...v,
        search: this.filters[this.layer.id]?.["search"] ? this.filters[this.layer.id]["search"] : "",
      };

      this.fieldFilters = v;
      this.$emit("update-filters", newFilters);
    },
    resetFieldFilters() {
      this.fieldFilters = {};
      this.selectedFilterProperties = [];
      this.$emit("update-filters", {});
    },
    toggleFilters() {
      this.showFilters = !this.showFilters;

      if (this.showFilters) {
        this.filterFeatures = this.featureCollection.features;
      } else {
        this.resetFieldFilters();
      }
    },
    removeFilter(filter) {
      if (filter in this.fieldFilters) {
        delete this.fieldFilters[filter];
        this.fetchFeatures();
      }
    },
    headerText(property) {
      return this.layer.friendly_fields && this.layer.friendly_fields[property]
        ? this.layer.friendly_fields[property]
        : property;
    },
  },
};
</script>

<style scoped>
.filter-table-container {
  display: flex;
  flex-flow: column;
  max-height: calc(100 * var(--vh) - 10rem);
}

.filter-container {
  flex: 0 1 auto;
}

.table-wrapper td:first-child {
  width: var(--width-button-large);
  padding-left: 4px;
}

tbody > tr:hover {
  background-color: var(--color-grey-40);
}

.table-border {
  border: solid 1px var(--color-grey-60);
  border-radius: 6px;
}

.table-margin {
  margin-top: 20px;
}

.filter-label-padding {
  padding-left: 8px;
}

.selected-filter-container {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
  flex-wrap: wrap;
}

.filter-padding {
  padding-top: 10px;
}

.filter-grid {
  display: grid;
  grid-template-columns: clamp(200px, 35%, 400px) auto;
  grid-template-rows: auto;
  grid-gap: 1rem;
  align-items: end;
}

@media (max-width: 576px) {
  .filter-grid {
    display: grid;
    grid-template-columns: 1fr;
    grid-template-rows: auto;
    grid-gap: 1rem;
  }

  .selected-filter-container {
    justify-content: flex-start;
    flex-direction: column;
  }
}

.toggle-filter-container {
  display: flex;
  justify-content: flex-start;
  align-items: center;
  gap: 6px;
}

.total-results {
  margin-bottom: 0;
}
</style>
