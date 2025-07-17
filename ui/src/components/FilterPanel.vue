<template>
  <PanelDisplay
    title="Verfijn resultaten"
    :loading="loading"
    :badge="countOfActiveSelectedFiltersForLayer"
    @hidePanel="hidePanel"
  >
    <p v-if="facets.length <= 0 || !layer" class="info-text">Er zijn nog geen filters geconfigureerd.</p>
    <div v-if="layer">
      <ExpandButton v-for="facet in facets" :key="facet" :title="getTitle(facet)" is-open>
        <ul v-if="facetValues[facet]">
          <li v-for="value in facetValues[facet]" :key="value">
            <CheckboxField
              :name="facet"
              :value="value"
              :checked="
                store.layerFilters &&
                store.layerFilters[layer.id] &&
                store.layerFilters[layer.id]['filters'][facet] &&
                store.layerFilters[layer.id]['filters'][facet].includes(value)
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
import { useMapStore } from "@/stores/map_store";
import { formatRawString } from "@/utils/string-helpers";
import CheckboxField from "./CheckboxField";
import ExpandButton from "./ExpandButton";
import PanelDisplay from "./PanelDisplay";

export default {
  name: "FilterPanel",
  components: {
    PanelDisplay,
    ExpandButton,
    CheckboxField,
  },
  props: {
    mapId: String,
    facets: Array,
    layer: Object,
    user: Object,
  },
  emits: ["hidePanel"],
  data() {
    return {
      facetValues: {},
      loading: false,
      store: null,
    };
  },
  computed: {
    countOfActiveSelectedFiltersForLayer() {
      return this.store && this.facets
        ? this.store.getActiveSelectedItemCountPerFilterForLayer(this.layer?.id, this.facets)
        : 0;
    },
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
  created() {
    this.store = useMapStore(this.mapId);
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
      const { name, value, checked } = e.target;

      let newFilters = this.store.getFiltersForLayer(this.layer.id);

      if (!newFilters[name]) {
        newFilters[name] = [];
      }

      if (checked && !newFilters[name].includes(value)) {
        newFilters[name].push(value);
      }

      if (!checked && newFilters[name].includes(value)) {
        newFilters[name] = newFilters[name].filter((v) => v !== value);
      }

      // somehow there sometimes ends up an element with key "undefined" in newFilters, this breaks Atlas. We also don't want filterKeys in this array with no values.
      delete newFilters["undefined"];

      this.store.updateFiltersForLayer(this.layer.id, newFilters);
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
