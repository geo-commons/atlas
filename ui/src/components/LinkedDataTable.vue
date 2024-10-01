<template>
  <ExpandButton :title="computedTitle" :is-open="isOpen" @show-content="onShowContentChange">
    <template #default>
      <div>
        <span v-if="error">{{ error }}</span>
        <span v-if="loading">Bezig met laden...</span>
        <span v-if="!loading && !error && displayProperties.length === 0">Geen weergave beschikbaar.</span>
        <div v-if="!loading && !error && displayProperties.length > 0">
          <div class="table-wrapper">
            <table class="linked-data-table">
              <thead>
                <tr>
                  <th class="linked-data-header"></th>
                  <th v-if="linkedData.use_detail_view" class="linked-data-header"></th>
                  <th v-for="(property, i) in tableHeaders" :key="property" class="linked-data-header">
                    <StackSortableTableHeaderItem
                      :header-text="headerText(property)"
                      :property="displayProperties[i]"
                      :sort-stack="sortStack"
                      @sort="(column, ascending) => sortColumn(column, ascending)"
                    />
                  </th>
                </tr>
              </thead>
              <tbody>
                <tr v-for="feature in features" :key="feature.id">
                  <td class="linked-data-cell">
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
                  <td v-if="linkedData.use_detail_view" class="linked-data-cell">
                    <button
                      v-tippy="{ placement: 'right' }"
                      class="iconbutton __small __round"
                      content="Toon meer informatie"
                      @click="selectRow(feature)"
                    >
                      <InformationCircleIcon class="icon __small" />
                    </button>
                  </td>
                  <td v-for="property in displayProperties" :key="property" class="linked-data-cell">
                    <RichValue :data-key="property" :data-value="feature.properties[property]" />
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </template>
  </ExpandButton>
</template>

<script>
import GeoJSON from "ol/format/GeoJSON";

import ExpandButton from "./ExpandButton";
import StackSortableTableHeaderItem from "./StackSortableTableHeaderItem.vue";
import { getFeatureCenterCoordinates } from "@/utils/geometry-helpers";
import MarkerIcon from "@/assets/icons/marker-icon.svg";
import InformationCircleIcon from "@/assets/icons/information-circle-icon.svg";
import { formatRawString } from "@/utils/string-helpers";
import RichValue from "@/components/RichValue.vue";

// todo: check if headers need to be sortable

export default {
  name: "LinkedDataTable",
  components: {
    RichValue,
    InformationCircleIcon,
    MarkerIcon,
    ExpandButton,
    StackSortableTableHeaderItem,
  },
  props: {
    linkedData: Object,
    isOpen: Boolean,
    initialTableHeaders: Array,
    overallFilter: Object,
    position: Object,
    user: Object,
  },
  data() {
    return {
      features: [],
      displayProperties: [],
      loading: false,
      error: "",
      numberMatched: null,
      loadContent: true,
      sortStack: [],
    };
  },
  computed: {
    computedTitle() {
      if (this.numberMatched !== null) {
        return `${this.linkedData.title} (${this.numberMatched})`;
      }

      return this.linkedData.title;
    },
    tableHeaders() {
      if (!this.initialTableHeaders.length && this.features) {
        return Object.keys(this.features[0].properties);
      }

      return this.initialTableHeaders;
    },
  },
  watch: {
    isOpen: "fetchFeatures",
    sortStack: {
      handler() {
        this.fetchFeatures();
      },
      deep: true,
    },
  },
  mounted() {
    this.fetchFeatures();
  },
  methods: {
    onShowContentChange(value) {
      if (!value) {
        return;
      }

      this.loadContent = true;
      this.fetchFeatures();
    },
    async fetchFeatures() {
      this.loading = true;
      this.error = "";

      const params = new URLSearchParams([
        ["service", "WFS"],
        ["version", "1.0.0"],
        ["request", "GetFeature"],
        ["typename", this.linkedData.name],
        ["outputFormat", "application/json"],
        ["maxFeatures", "5000"],
      ]);

      if (this.overallFilter) {
        params.set("cql_filter", `${this.overallFilter.key} = '${this.overallFilter.value}'`);
      }

      if (this.sortStack.length > 0) {
        let sortString = [];

        this.sortStack.forEach((attr) => {
          sortString.push(`${attr.id} ${attr.asc ? "A" : "D"}`);
        });

        params.set("sortBy", sortString);
      }

      try {
        const url = new URL(this.linkedData.url);
        url.search = params.toString();

        const result = await fetch(url.toString(), this.getFetchParameters());

        if (!result.ok) {
          if (result.status === 401) {
            this.error = "U moet ingelogd zijn om deze data te bekijken.";
          } else if (result.status === 403) {
            this.error = "U heeft geen rechten om deze data te bekijken.";
          } else {
            this.error = "Er is een fout opgetreden tijdens het ophalen van de gegevens.";
          }

          this.loading = false;
          return;
        }

        const data = await result.json();

        this.features = data.features;
        this.numberMatched = data.numberMatched;

        if (this.displayProperties.length === 0 && data.features.length > 0) {
          // cache first retrieval of properties into this.displayProperties
          const fetchedProperties = Object.keys(data.features[0].properties);

          this.displayProperties =
            this.linkedData.display_properties.length > 0 ? this.linkedData.display_properties : fetchedProperties;
        }
      } catch (e) {
        console.error(e);
        this.error = "Er is een fout opgetreden tijdens het ophalen van de gegevens.";
        this.features = [];
        this.displayProperties = [];
        this.searchProperties = [];
        this.numberMatched = 0;
      }

      this.loading = false;
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
      if (this.linkedData.source && this.linkedData.source.authenticate && this.user && this.user.token) {
        return {
          headers: { Authorization: `Bearer ${this.user.token}` },
        };
      }

      return {};
    },
    selectRow(feature) {
      const detailViewFields = this.getDetailViewFields(feature);

      feature = {
        title: this.linkedData.title,
        properties: feature.properties,
        detailViewFields: detailViewFields,
      };
      this.$emit("select-feature-details", feature);
    },
    getDetailViewFields(feature) {
      if (this.linkedData.detail_view_fields.length > 0) {
        return this.linkedData.detail_view_fields;
      }

      return Object.keys(feature.properties);
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
    headerText(property) {
      if (this.linkedData.friendly_fields && this.linkedData.friendly_fields[property]) {
        return this.linkedData.friendly_fields[property];
      }

      return formatRawString(property);
    },
  },
};
</script>

<style scoped>
.table-wrapper {
  word-wrap: break-word;
  overflow: auto;
  flex: 1 1 auto;
}

.linked-data-table {
  font-size: var(--font-size-small);
  overflow-x: auto;
  border-collapse: collapse;
  width: 100%;
}

.linked-data-cell {
  padding: 4px;
  text-align: left;
  height: 30px;
  border-bottom: 1px solid var(--color-grey-60);
}

.linked-data-table tbody tr:hover {
  background-color: var(--color-grey-40);
}

.linked-data-header {
  font-weight: var(--font-weight-normal);
  color: var(--color-text-grey);
  padding: 8px 4px;
  border-bottom: 1px solid var(--color-grey-60);
  text-align: left;
}

.__marker {
  stroke: currentColor;
  stroke-width: 2px;
  fill: white;
}
</style>
