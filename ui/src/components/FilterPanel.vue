<template>
  <PanelDisplay title="Verfijn resultaten" :loading="loading" @hidePanel="hidePanel">
    <p v-if="facets.length <= 0 || !layer" class="info-text">Er zijn nog geen filters geconfigureerd.</p>
    <div v-if="layer">
      <ExpandButton v-for="facet in facets" :key="facet" :title="getTitle(facet)" is-open>
        <ul v-if="facetValues[facet]">
          <li v-for="value in facetValues[facet]" :key="value">
            <CheckboxField
              :name="facet"
              :value="value"
              :checked="
                filters && filters[layer.id] && filters[layer.id][facet] && filters[layer.id][facet].includes(value)
              "
              @click="onChangeFilter"
            />
          </li>
        </ul>
      </ExpandButton>
    </div>
  </PanelDisplay>
</template>

<script>
import PanelDisplay from "./PanelDisplay";
import ExpandButton from "./ExpandButton";
import CheckboxField from "./CheckboxField";
import { formatRawString } from "@/utils/string-helpers";

export default {
  name: "FilterPanel",
  components: {
    PanelDisplay,
    ExpandButton,
    CheckboxField,
  },
  props: {
    facets: Array,
    layer: Object,
    user: Object,
    filters: Object,
  },
  emits: ["hidePanel", "update-filters"],
  data() {
    return {
      facetValues: {},
      loading: false,
    };
  },
  watch: {
    facets: {
      handler() {
        this.fetchFacetValues();
      },
      deep: true,
    },
  },
  mounted() {
    this.fetchFacetValues();
  },
  methods: {
    hidePanel() {
      this.$emit("hidePanel");
    },
    async fetchFacetValues() {
      if (!this.layer || !this.facets || !this.facets.length > 0) {
        return;
      }

      this.loading = true;

      const params = new URLSearchParams([
        ["service", "WFS"],
        ["version", "1.0.0"],
        ["request", "GetFeature"],
        ["typename", this.layer.name],
        ["outputFormat", "application/json"],
      ]);

      const facetValues = {};

      try {
        const url = new URL(this.layer.url);
        url.search = params.toString();

        const result = await fetch(url.toString(), this.getFetchParameters());
        const data = await result.json();

        this.facets.forEach((facet) => {
          facetValues[facet] = [];
        });

        data.features.forEach((feature) => {
          this.facets.forEach((facet) => {
            if (!feature.properties[facet]) {
              return;
            }

            const value = feature.properties[facet];
            if (!facetValues[facet].includes(value) && facetValues[facet].length < 100) {
              facetValues[facet].push(value);
            }
          });
        });

        this.facets.forEach((facet) => {
          facetValues[facet].sort();
        });
      } catch (e) {
        console.error(e);
      }

      this.facetValues = facetValues;
      this.loading = false;
    },
    getFetchParameters() {
      if (this.layer.source && this.layer.source.authenticate && this.user && this.user.token) {
        return {
          headers: { Authorization: `Bearer ${this.user.token}` },
        };
      }

      return {};
    },
    onChangeFilter(e) {
      let newFilters = { ...this.filters };

      if (!newFilters[this.layer.id]) {
        newFilters[this.layer.id] = {};
      }

      if (!newFilters[this.layer.id][e.target.name]) {
        newFilters[this.layer.id][e.target.name] = [];
      }

      if (e.target.checked && !newFilters[this.layer.id][e.target.name].includes(e.target.value)) {
        newFilters[this.layer.id][e.target.name].push(e.target.value);
      }

      if (!e.target.checked && newFilters[this.layer.id][e.target.name].includes(e.target.value)) {
        newFilters[this.layer.id][e.target.name] = newFilters[this.layer.id][e.target.name].filter(
          (v) => v !== e.target.value,
        );
      }

      this.$emit("update-filters", newFilters);
    },
    getTitle(facet) {
      if (this.layer.friendly_fields && this.layer.friendly_fields[facet]) {
        return this.layer.friendly_fields[facet];
      }

      return formatRawString(facet);
    },
  },
};
</script>

<style scoped>
.info-text {
  margin: 30px 20px;
}
</style>
