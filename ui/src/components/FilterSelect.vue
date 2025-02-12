<template>
  <div v-if="filterOptions && filterProperty" class="flex __column filter-width">
    <label :for="filterProperty" class="filter-label-padding">{{
      filterPropertyDisplayName ? filterPropertyDisplayName : filterProperty
    }}</label>
    <multi-select
      v-if="!filterOnId"
      v-model="selectedItems"
      :options="currentFilterOptions"
      :virtual-scroller-options="{ itemSize: 50 }"
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
      :virtual-scroller-options="{ itemSize: 50 }"
      placeholder="Kies waarde"
      filter-placeholder="Zoek waarde"
      filter
      @update:modelValue="updateFieldFilters()"
    />
  </div>
</template>

<script>
import { useMapStore } from "@/stores/map_store";

export default {
  name: "FilterSelect",
  props: {
    filterOptions: Array,
    fieldFilters: Object,
    filterProperty: String,
    mapId: String,
    layerId: String,
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
      store: null,
      currentFilterOptions: this.filterOptions,
    };
  },
  watch: {
    filterOptions(value) {
      this.currentFilterOptions = value;
    },
  },
  created() {
    this.store = useMapStore(this.mapId);

    const filterProperties = this.store.layerFilters[this.layerId]?.filters?.[this.filterProperty]
      ? this.store.layerFilters[this.layerId].filters[this.filterProperty]
      : [];

    this.selectedItems = filterProperties;

    this.store.$subscribe((mutation, state) => {
      const filterProperties = state.layerFilters[this.layerId]?.filters?.[this.filterProperty] || [];

      this.selectedItems = filterProperties;
    });
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

      const newFieldFilter = { ...this.fieldFilters, [this.filterProperty]: this.selectedItems };

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
