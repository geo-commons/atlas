<template>
  <Spinner v-if="loading" />
  <div v-else-if="error && errorMessage">{{ errorMessage }}</div>
  <div v-else-if="error">Er is iets fout gegaan bij het ophalen van de data...</div>
  <div v-else class="filter-table-container">
    <div class="filter-container">
      <div class="toggle-filter-container">
        <switch-slider
          :initial-checked-status="showFilters"
          :aria-label="`${showFilters ? 'Deactiveer' : 'Activeer'} filters voor laag ${layer.title}`"
          @toggle-switch="toggleFilters()"
        />
        <div>{{ showFilters ? "Deactiveer" : "Activeer" }} filters voor {{ layer.title.toLowerCase() }}</div>
      </div>
      <div v-if="showFilters" class="filter-padding filter-grid">
        <div>
          <label for="selected_columns" class="filter-label-padding tw-pt-2">Kolom(men) om op te filteren</label>
          <multi-select
            id="selected_columns"
            v-model="selectedFilterProperties"
            :style="{ maxWidth: 'clamp(200px,100%,400px)', minWidth: 'clamp(200px, 100%, 400px)' }"
            :options="filterProperties"
            :placeholder="'Kies kolom(men)'"
            filter
            display="chip"
            filter-placeholder="Zoek kolom"
            :pt="{
              label: {
                class: ['!tw-flex tw-flex-wrap'],
              },
            }"
          />
        </div>
        <div v-if="selectedFilterProperties" class="selected-filter-container">
          <div v-for="property in selectedFilterProperties" :key="property">
            <FilterSelect
              :map-id="mapId"
              :layer-id="layer.id"
              :filter-options="filterOptions[property]"
              :field-filters="fieldFilters"
              :filter-property="property"
              @on-filter-change="(v) => setFieldFilters(v, property)"
            />
          </div>
        </div>
      </div>
    </div>

    <table-list class="table table-wrapper table-border table-margin">
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
                <MarkerIcon class="icon __small __marker" />
              </button>
            </td>
            <td v-for="property in displayProperties" :key="property">
              <RichValue :data-key="property" :data-value="feature.properties[property]" />
            </td>
          </tr>
        </tbody>
      </table>
    </table-list>
    <div class="tw-flex tw-flex-col md:tw-flex-row tw-justify-center md:tw-relative">
      <p v-if="numberMatched !== null" class="total-results md:tw-left-0 md:tw-absolute">
        {{ numberMatched }} {{ numberMatched === 1 ? "resultaat" : "resultaten" }}
      </p>
      <Paginator
        :template="{
          '640px': 'FirstPageLink PrevPageLink CurrentPageReport NextPageLink LastPageLink',
          default: 'FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink RowsPerPageDropdown',
        }"
        :current-page-report-template="'({currentPage} van {totalPages})'"
        :rows="pageState.rows"
        :total-records="numberMatched"
        :first="pageState.page * pageState.rows - 1 + pageState.rows"
        :rows-per-page-options="[10, 20, 30, 50, 100]"
        @page="updatePageState"
      ></Paginator>
    </div>
  </div>
</template>

<script>
import Cookies from "js-cookie";
import TableList from "./TableList.vue";
import GeoJSON from "ol/format/GeoJSON";
import { getFeatureCenterCoordinates } from "@/utils/geometry-helpers";
import FilterSelect from "./FilterSelect.vue";
import SwitchSlider from "./SwitchSlider.vue";
import MarkerIcon from "../assets/icons/marker-icon.svg";
import { getFetchParameters } from "../utils/auth";
import StackSortableTableHeaderItem from "@/components/StackSortableTableHeaderItem.vue";
import { formatRawString } from "@/utils/string-helpers";
import RichValue from "@/components/RichValue.vue";
import Spinner from "@/components/Spinner.vue";
import { useMapStore } from "@/stores/map_store";
import { WKT } from "ol/format";
import { useToast } from "primevue";

export default {
  name: "FeatureTable",
  components: {
    RichValue,
    StackSortableTableHeaderItem,
    TableList,
    MarkerIcon,
    FilterSelect,
    SwitchSlider,
    Spinner,
  },
  props: {
    layer: Object,
    position: Object,
    searchValue: String,
    mapId: String,
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
      numberMatched: null,
      sortStack: [],
      searchProperties: [],
      pageState: {
        page: 0,
        first: 20,
        rows: 20,
        pageCount: 4,
      },
      error: false,
      errorMessage: null,
      loading: true,
      isDownloadPending: false,
      toast: useToast(),
    };
  },
  watch: {
    searchValue() {
      this.fetchFeatures();

      // If searchValue gets deleted or removed, set searchValue to an empty string
      if (!this.searchValue) {
        this.store.updateSearchQueryForLayer(this.layer.id, "");
      }
    },
    selectedArea: "fetchFeatures",
    filter: "fetchFeatures",
    fieldFilters: {
      handler() {
        this.showFilters = !!Object.keys(this.fieldFilters).length;

        this.fetchFeatures();
      },
      deep: true,
    },
    pageState: "fetchFeatures",
    sortStack: {
      handler() {
        this.fetchFeatures();
      },
      deep: true,
    },
    selectedFilterProperties(newValue, oldValue) {
      const listWithRemovedFilters = oldValue.filter((value) => !newValue.includes(value));
      const newFilterProperty = newValue.filter((value) => !oldValue.includes(value));

      newFilterProperty.map((newFilterProperty) => {
        this.getFilterOptions(newFilterProperty);
      });

      listWithRemovedFilters.map((removedFilter) => {
        this.removeFilter(removedFilter);
      });
    },
  },
  async created() {
    this.store = useMapStore(this.mapId);

    await this.fetchFilterProperties();
    await this.fetchSearchProperties();

    const filters = this.store.getFiltersForLayer(this.layer.id);

    this.showFilters = !!Object.keys(this.fieldFilters).length;

    this.fieldFilters = filters;

    this.selectedFilterProperties = Object.keys(filters);

    this.store.$subscribe((_, state) => {
      // From the moment this store subscription is created,
      // when the filters for the relevant layer change, both the
      // filter properties (selectedFilterProperties) and filter values (fieldFilters) are updated.
      if (state.layerFilters[this.layer.id]) {
        this.fieldFilters = state.layerFilters[this.layer.id]?.filters || {};
        this.selectedFilterProperties = Object.keys(state.layerFilters[this.layer.id]?.filters || []);
      }
    });

    await this.fetchFeatures();
  },
  methods: {
    async fetchFeatures() {
      this.error = false;
      this.errorMessage = null;

      const params = new URLSearchParams([
        ["service", "WFS"],
        ["version", "1.0.0"],
        ["request", "GetFeature"],
        ["typename", this.layer.name],
        ["outputFormat", "application/json"],
        ["maxFeatures", this.pageState.rows],
        ["startIndex", this.pageState.rows * this.pageState.page],
      ]);

      const filters = [];

      if (this.searchValue && this.searchProperties.length > 0) {
        const searchQuery = `(${this.searchProperties.map((key) => `${key} ILIKE '%${this.searchValue}%'`).join(" OR ")})`;

        filters.push(searchQuery);

        this.store.updateSearchQueryForLayer(this.layer.id, searchQuery);
      }

      if (this.fieldFilters && Object.keys(this.fieldFilters).length > 0) {
        Object.keys(this.fieldFilters).forEach((key) => {
          const values = this.fieldFilters[key];
          if (values.length > 0) {
            const filterOnEmptyValues = values.includes("Leeg");
            const nonEmptyValues = values.filter((f) => f !== "Leeg");
            let valueFilters = [];

            if (nonEmptyValues.length > 0) {
              valueFilters.push(`${key} in (${nonEmptyValues.map((f) => this.replaceQuotes(f)).join(",")})`);
            }
            if (filterOnEmptyValues) {
              valueFilters.push(`(${key} IS NULL or ${key} = '')`);
            }

            if (valueFilters.length > 0) {
              filters.push(`(${valueFilters.join(" OR ")})`);
            }
          }
        });
      }

      if (this.selectedArea) {
        const wkt = new WKT();
        const geom = wkt.writeGeometry(this.selectedArea);

        const fullFilter = `WITHIN(geom,${geom})`;
        const encodedLength = encodeURIComponent(fullFilter).length;
        if (encodedLength <= 32000) {
          filters.push(fullFilter);
        } else {
          this.error = true;
          this.errorMessage =
            "Het geselecteerde gebied is momenteel te complex om te gebruiken als filter. Probeer een eenvoudiger gebied te selecteren of verklein het bestaande gebied.";
          this.loading = false;
          return;
        }
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

        const fetchParams = getFetchParameters(this.layer, this.user);
        const result = await fetch(url.toString(), fetchParams);

        const data = await result.json();

        this.featureCollection = data;

        this.numberMatched = data.numberMatched;
      } catch (e) {
        console.error(e);
        this.error = true;
        this.featureCollection = { features: [] };
        this.searchProperties = [];
        this.numberMatched = 0;
      }

      this.loading = false;
    },
    async fetchFilterProperties() {
      this.error = false;

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

        const fetchedProperties = featureType.properties.map((p) => p.name);
        this.displayProperties =
          this.layer.display_properties.length > 0 ? this.layer.display_properties : fetchedProperties;

        this.filterProperties = [...this.displayProperties];
      } catch (e) {
        console.error(e);
        this.error = true;
        this.displayProperties = [];
        this.searchProperties = [];
      }
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
    async fetchFeaturesForDownload() {
      this.error = false;

      const params = new URLSearchParams([
        ["service", "WFS"],
        ["version", "1.0.0"],
        ["request", "GetFeature"],
        ["typename", this.layer.name],
        ["outputFormat", "application/json"],
      ]);

      const filters = [];

      if (this.searchValue && this.searchProperties.length > 0) {
        const searchQuery = `(${this.searchProperties.map((key) => `${key} ILIKE '%${this.searchValue}%'`).join(" OR ")})`;

        filters.push(searchQuery);

        this.store.updateSearchQueryForLayer(this.layer.id, searchQuery);
      }

      if (this.fieldFilters && Object.keys(this.fieldFilters).length > 0) {
        Object.keys(this.fieldFilters).forEach((key) => {
          if (this.fieldFilters[key].length) {
            filters.push(`${key} in (${this.fieldFilters[key].map((f) => this.replaceQuotes(f)).join(",")})`);
          }
        });
      }

      if (this.selectedArea) {
        const wkt = new WKT();
        const geom = wkt.writeGeometry(this.selectedArea);

        const fullFilter = `WITHIN(geom,${geom})`;
        const encodedLength = encodeURIComponent(fullFilter).length;
        if (encodedLength <= 32000) {
          filters.push(fullFilter);
        } else {
          this.error = true;
          this.errorMessage =
            "Het geselecteerde gebied is momenteel te complex om te gebruiken als filter. Probeer een eenvoudiger gebied te selecteren of verklein het bestaande gebied.";
          this.loading = false;
          return;
        }
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

        const fetchParams = getFetchParameters(this.layer, this.user);

        const result = await fetch(url.toString(), fetchParams);

        return await result.json();
      } catch (e) {
        console.error("Er is iets fout gegaan bij het ophalen van de data voor de download", e);
      }

      this.loading = false;
      return [];
    },
    async downloadCSV() {
      if (!this.layer.is_exportable) {
        this.toast.add({
          severity: "error",
          summary: "Downloaden mislukt",
          detail: "Deze kaartlaag is niet exporteerbaar.",
          life: 5000,
        });
        return;
      }

      this.isDownloadPending = true;

      const separator = ";";
      const filename = this.layer.title
        .replace(" ", "-")
        .replace(/[^a-z0-9-]/gi, "")
        .toLowerCase();

      const fetchDownloadData = await this.fetchFeaturesForDownload();

      let data = this.displayProperties.map((property) => `"${property.replace(/"/g, '""')}"`).join(separator) + "\n";

      fetchDownloadData.features.forEach((feature) => {
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

      this.isDownloadPending = false;
    },
    async download(outputFormat) {
      if (!this.layer.is_exportable) {
        this.toast.add({
          severity: "error",
          summary: "Downloaden mislukt",
          detail: "Deze kaartlaag is niet exporteerbaar.",
          life: 5000,
        });
        return;
      }

      this.isDownloadPending = true;

      const fetchDownloadData = await this.fetchFeaturesForDownload();

      const result = await fetch(`/atlas/convert/${outputFormat}`, {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
        body: JSON.stringify({
          outputFormat,
          featureCollection: fetchDownloadData,
        }),
      });

      if (!result.ok) {
        const response = await result.json();

        this.toast.add({
          severity: "error",
          summary: "Downloaden mislukt",
          detail: response.error,
          life: 5000,
        });

        this.isDownloadPending = false;
        return;
      }

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

      this.isDownloadPending = false;
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

      this.$emit(
        "set-position",
        {
          ...this.position,
          marker: center,
          zoom: 19,
        },
        false,
        false,
      );

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
    async fetchFilterOptionsForProperty(property) {
      const params = new URLSearchParams([
        ["service", "WFS"],
        ["version", "1.0.0"],
        ["request", "GetFeature"],
        ["typename", this.layer.name],
        ["outputFormat", "application/json"],
        ["cql_filter", `${property} IS NOT NULL`],
        ["propertyName", property],
        ["sortBy", property],
      ]);
      try {
        const url = new URL(this.layer.url);
        url.search = params.toString();

        const result = await fetch(url.toString(), getFetchParameters(this.layer, this.user));

        if (result.ok) {
          const data = await result.json();
          return data.features;
        }
      } catch (e) {
        console.error(e);
      }

      return [];
    },
    async getFilterOptions(property) {
      if (this.filterOptions[property]) {
        return this.filterOptions[property];
      }

      const fetchedFeatureFilters = await this.fetchFilterOptionsForProperty(property);
      // Extract the unique values from the fetched features
      const filters = Array.from(new Set(fetchedFeatureFilters.map((feature) => feature.properties[property]))).filter(
        (filter) => filter !== null && (typeof filter !== "string" || filter.trim() !== ""),
      );

      this.filterOptions[property] = ["Leeg", ...filters];
    },
    setFieldFilters(v) {
      this.fieldFilters = v;

      this.store.updateFiltersForLayer(this.layer.id, v);
    },
    toggleFilters() {
      this.showFilters = !this.showFilters;

      if (this.showFilters) {
        this.filterFeatures = this.featureCollection.features;
      }

      if (!this.showFilters) {
        this.store.updateFiltersForLayer(this.layer.id, {});
      }
    },
    removeFilter(filter) {
      if (filter in this.fieldFilters) {
        delete this.fieldFilters[filter];
        this.fetchFeatures();
      }
    },
    headerText(property) {
      if (this.layer.friendly_fields && this.layer.friendly_fields[property]) {
        return this.layer.friendly_fields[property];
      }

      return formatRawString(property);
    },
    updatePageState(updatedPageState) {
      this.pageState = updatedPageState;
    },
  },
};
</script>

<style scoped>
.filter-table-container {
  display: flex;
  flex-flow: column;
  max-width: 100%;
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
  align-items: start;
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
