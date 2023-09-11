<template>
  <div v-if="filters && filterProperty" class="flex-column filter-min-width">
    <label :for="filterProperty" class="filter-label-padding">{{
      filterProperty
    }}</label>
    <multiselect
      :id="filterProperty"
      v-model="selectedItems"
      :options="filters"
      placeholder="Kies waarde"
      :show-labels="false"
      open-direction="bottom"
      @input="updateFieldFilters()"
    />
  </div>
</template>

<script>
import Multiselect from "vue-multiselect";

export default {
  name: "FilterSelect",

  components: { Multiselect },
  props: {
    featureCollection: Object,
    fieldFilters: Object,
    filterProperty: String,
  },
  data() {
    return {
      selectedItems: "",
      filters: null,
    };
  },
  computed: {},
  mounted() {
    this.getFiltersByProperty();
  },
  methods: {
    updateFieldFilters() {
      if (this.selectedItems) {
        this.$emit("onFilterChange", {
          ...this.fieldFilters,
          [this.filterProperty]: this.selectedItems,
        });
        return;
      }

      const newFieldFilter = { ...this.fieldFilters };
      delete newFieldFilter[this.filterProperty];
      this.$emit("onFilterChange", newFieldFilter);
    },
    getFiltersByProperty() {
      // initialize filters for relevant feature property
      if (!this.filters) {
        let featurePropSet = new Set();

        if (this.featureCollection.features && this.filterProperty) {
          this.featureCollection.features.forEach((feature) => {
            if (feature.properties[this.filterProperty]) {
              featurePropSet.add(feature.properties[this.filterProperty]);
            }
          });
        }
        this.filters = [...featurePropSet];
      }

      return this.filters;
    },
  },
};
</script>
<style scoped>
.filter-min-width {
  min-width: 125px;
}

.filter-label-padding {
  padding-left: 8px;
}
</style>
