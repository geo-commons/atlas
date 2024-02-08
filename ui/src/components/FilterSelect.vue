<template>
  <div v-if="filterOptions && filterProperty" class="flex __column filter-width">
    <label :for="filterProperty" class="filter-label-padding">{{
      filterPropertyDisplayName ? filterPropertyDisplayName : filterProperty
    }}</label>
    <multiselect
      v-if="!filterOnId"
      :id="filterProperty"
      v-model="selectedItems"
      :options="currentFilterOptions"
      placeholder="Kies waarde"
      tag-placeholder="Enter voor nieuwe waarde"
      :show-labels="false"
      :multiple="true"
      :taggable="true"
      open-direction="bottom"
      @input="updateFieldFilters()"
      @tag="addFacetValue"
    />
    <multiselect
      v-else
      :id="filterProperty"
      v-model="selectedItems"
      :track-by="trackBy"
      :label="label"
      :options="currentFilterOptions"
      placeholder="Kies waarde"
      tag-placeholder="Enter voor nieuwe waarde"
      :show-labels="false"
      :multiple="true"
      :taggable="true"
      open-direction="bottom"
      @input="updateFieldFilters()"
      @tag="addFacetValue"
    />
  </div>
</template>

<script>
import Multiselect from "vue-multiselect";

export default {
  name: "FilterSelect",
  components: { Multiselect },
  props: {
    filterOptions: Array,
    fieldFilters: Object,
    filterProperty: String,
    filterPropertyDisplayName: String,
    filterOnId: {
      type: Boolean,
      default: false,
    },
    trackBy: String,
    label: String,
  },
  data() {
    return {
      selectedItems: [],
      currentFilterOptions: this.filterOptions,
    };
  },
  methods: {
    updateFieldFilters() {
      if (this.selectedItems.length > 0) {
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
    addFacetValue(newTag) {
      this.currentFilterOptions.push(newTag);
      this.selectedItems.push(newTag);
      this.updateFieldFilters();
    },
  },
};
</script>
<style scoped>
.filter-width {
  min-width: 125px;
  max-width: 225px;
}

.filter-label-padding {
  padding-left: 8px;
}

@media (max-width: 576px) {
  .filter-width {
    width: 100%;
    max-width: 100%;
  }
}
</style>
