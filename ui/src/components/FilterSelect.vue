<template>
  <div v-if="filterOptions && filterProperty" class="flex-column filter-min-width">
    <label :for="filterProperty" class="filter-label-padding">{{
      filterPropertyDisplayName ? filterPropertyDisplayName : filterProperty
    }}</label>
    <multiselect
      :id="filterProperty"
      v-model="selectedItems"
      :options="filterOptions"
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
    filterOptions: Array,
    fieldFilters: Object,
    filterProperty: String,
    filterPropertyDisplayName: String,
  },
  data() {
    return {
      selectedItems: "",
    };
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

@media (max-width: 576px) {
  .filter-min-width {
    width: 100%;
  }
}
</style>
