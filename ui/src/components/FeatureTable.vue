<template>
  <table-list class="table table-border">
    <table>
      <thead>
        <tr>
          <th></th>
          <th v-for="property in displayProperties" :key="property">
            <FeatureTableHeaderItem
              :layer="layer"
              :property="property"
              :field-filters="fieldFilters"
              :sort-key="sortKey"
              :sort-ascending="sortAscending"
              @change="(filter) => (fieldFilters = filter)"
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
              <PinIcon />
            </button>
          </td>
          <td v-for="property in displayProperties" :key="property">
            {{ feature.properties[property] }}
          </td>
        </tr>
      </tbody>
    </table>
  </table-list>
</template>

<script>
import Cookies from "js-cookie";
import FeatureTableHeaderItem from "./FeatureTableHeaderItem.vue";
import TableList from "./TableList.vue";
import PinIcon from "../icons/PinIcon.vue";
import GeoJSON from "ol/format/GeoJSON";
import { getFeatureCenterCoordinates } from "../utils/geometry-helpers";

export default {
  name: "FeatureTable",
  components: {
    FeatureTableHeaderItem,
    TableList,
    PinIcon,
  },
  props: {
    layer: Object,
    position: Object,
    query: String,
    selectedArea: Object,
  },
  data() {
    return {
      sortKey: "",
      sortAscending: true,
      featureCollection: {
        features: [],
      },
      displayProperties: [],
      fieldFilters: {},
    };
  },
  computed: {
    sortedFeatures() {
      if (this.sortKey && this.featureCollection.features) {
        // eslint-disable-next-line vue/no-side-effects-in-computed-properties
        return this.featureCollection.features.sort((a, b) => {
          const textA = a.properties[this.sortKey];
          const textB = b.properties[this.sortKey];
          return this.sortAlphabetically(textA, textB, this.sortAscending);
        });
      }

      return this.featureCollection.features;
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
        filters.push(
          this.searchProperties
            .map((key) => `${key} ILIKE '%${this.query}%'`)
            .join(" OR ")
        );
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
        params.set(
          "cql_filter",
          `${this.overallFilter.key} = '${this.overallFilter.value}'`
        );
      }

      try {
        const url = new URL(this.layer.url);
        url.search = params.toString();

        const result = await fetch(url.toString(), this.getFetchParameters());
        const data = await result.json();

        this.featureCollection = data;
        this.numberMatched = data.numberMatched;

        if (this.displayProperties.length === 0 && data.features.length > 0) {
          // cache first retrieval of properties into this.displayProperties
          const fetchedProperties = Object.keys(data.features[0].properties);

          this.displayProperties =
            this.layer.display_properties.length > 0
              ? this.layer.display_properties
              : fetchedProperties;
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
      if (
        this.layer.search_properties &&
        this.layer.search_properties.length > 0
      ) {
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
        const stringProperties = featureType.properties.filter(
          (p) => p.localType === "string"
        );

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

      let data =
        this.displayProperties
          .map((property) => `"${property.replace(/"/g, '""')}"`)
          .join(separator) + "\n";

      this.featureCollection.features.forEach((feature) => {
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

    showFeature(feature) {
      const geometry = new GeoJSON().readFeature(feature).getGeometry();
      const center = getFeatureCenterCoordinates(feature);

      this.$emit("set-position", {
        ...this.position,
        marker: center,
      });

      this.$emit("on-fit", geometry.getExtent());
    },
    getFetchParameters() {
      if (
        this.layer.source &&
        this.layer.source.authenticate &&
        this.user &&
        this.user.token
      ) {
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

tbody > tr:hover {
  background-color: var(--color-grey-40);
}

.table-border {
  border: solid 1px var(--color-grey-60);
  border-radius: 6px;
}
</style>
