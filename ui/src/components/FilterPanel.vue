<template>
  <PanelDisplay title="Verfijn resultaten" @hidePanel="hidePanel">
    <p v-if="facets.length <= 0" class="info-text">
      Er zijn nog geen filters geconfigureerd.
    </p>

    <ExpandButton
      v-for="facet in facets"
      :key="facet"
      :title="
        layer.friendly_fields && layer.friendly_fields[facet]
          ? layer.friendly_fields[facet]
          : facet
      "
      is-open
    >
      <ul v-if="facetValues[facet]">
        <li v-for="value in facetValues[facet]" :key="value">
          <CheckboxField
            :name="facet"
            :value="value"
            :checked="
              filters &&
              filters[layer.id] &&
              filters[layer.id][facet] &&
              filters[layer.id][facet].includes(value)
            "
            @change="onChangeFilter"
          />
        </li>
      </ul>
    </ExpandButton>
  </PanelDisplay>
</template>

<script>
import PanelDisplay from "./PanelDisplay";
import ExpandButton from "./ExpandButton";
import CheckboxField from "./CheckboxField";

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
  data() {
    return {
      facetValues: {},
    };
  },
  watch: {
    facets: "fetchFacetValues",
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
            if (
              !facetValues[facet].includes(value) &&
              facetValues[facet].length < 100
            ) {
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
    onChangeFilter(e) {
      let newFilters = { ...this.filters };

      if (!newFilters[this.layer.id]) {
        newFilters[this.layer.id] = {};
      }

      if (!newFilters[this.layer.id][e.target.name]) {
        newFilters[this.layer.id][e.target.name] = [];
      }

      if (
        e.target.checked &&
        !newFilters[this.layer.id][e.target.name].includes(e.target.value)
      ) {
        newFilters[this.layer.id][e.target.name].push(e.target.value);
      }

      if (
        !e.target.checked &&
        newFilters[this.layer.id][e.target.name].includes(e.target.value)
      ) {
        newFilters[this.layer.id][e.target.name] = newFilters[this.layer.id][
          e.target.name
        ].filter((v) => v !== e.target.value);
      }

      this.$emit("update-filters", newFilters);
    },
  },
};
</script>

<style scoped>
.info-text {
  margin: 30px 20px;
}
</style>
