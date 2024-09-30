<template>
  <div v-if="filterOptions && filterProperty" class="flex __column filter-width">
    <label :for="filterProperty" class="filter-label-padding">{{
      filterPropertyDisplayName ? filterPropertyDisplayName : filterProperty
    }}</label>
    <multi-select
      v-if="!filterOnId"
      v-model="selectedItems"
      :options="currentFilterOptions"
      placeholder="Kies waarde"
      filter-placeholder="Zoek waarde"
      filter
      @update:modelValue="updateFieldFilters()"
    />
    <multi-select
      v-else
      v-model="selectedItems"
      :option-label="optionLabel"
      :options="currentFilterOptions"
      placeholder="Kies waarde"
      filter-placeholder="Zoek waarde"
      filter
      @update:modelValue="updateFieldFilters()"
    />
  </div>
</template>

<script>
export default {
  name: "FilterSelect",
  props: {
    filterOptions: Array,
    fieldFilters: Object,
    filterProperty: String,
    filterPropertyDisplayName: String,
    filterOnId: {
      type: Boolean,
      default: false,
    },
    optionLabel: String,
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
