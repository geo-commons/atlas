<template>
  <div v-if="filterOptions && filterProperty" class="flex __column filter-width">
    <label :for="filterProperty" class="filter-label-padding">{{
      filterPropertyDisplayName ? filterPropertyDisplayName : filterProperty
    }}</label>
    <Select
      :options="operatorOptions"
      v-model="selectedOperator"
      class="operator-select"
      @change="updateFieldFilters()"
      option-label="label"
      option-value="value"
    />
    <multi-select
      v-if="usesValueSelect && !filterOnId"
      v-model="selectedItems"
      :options="currentFilterOptions"
      :virtual-scroller-options="{ itemSize: 50 }"
      placeholder="Kies waarde"
      filter-placeholder="Zoek waarde"
      filter
      @update:model-value="updateFieldFilters()"
    />
    <multi-select
      v-else-if="usesValueSelect"
      v-model="selectedItems"
      :option-label="optionLabel"
      :options="currentFilterOptions"
      :virtual-scroller-options="{ itemSize: 50 }"
      placeholder="Kies waarde"
      filter-placeholder="Zoek waarde"
      filter
      @update:model-value="updateFieldFilters()"
    />
    <input
      v-else-if="usesTypedValue"
      :id="filterProperty"
      v-model="selectedValue"
      class="filter-value-input"
      placeholder="Vul waarde in"
      @input="updateFieldFilters()"
    />
  </div>
</template>

<script>
import { useMapStore } from "@/stores/map_store";
import { ELayerFilterOperator } from "@/types/mapStore";

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
  emits: ["onFilterChange"],
  data() {
    return {
      selectedItems: [],
      selectedOperator: ELayerFilterOperator.In,
      selectedValue: "",
      store: null,
      currentFilterOptions: this.filterOptions,
      operatorOptions: [
        { label: "is gelijk aan", value: ELayerFilterOperator.In },
        { label: "is niet gelijk aan", value: ELayerFilterOperator.NotIn },
        { label: "groter dan", value: ELayerFilterOperator.GreaterThan },
        { label: "groter dan of gelijk aan", value: ELayerFilterOperator.GreaterThanOrEqualTo },
        { label: "kleiner dan", value: ELayerFilterOperator.LessThan },
        { label: "kleiner dan of gelijk aan", value: ELayerFilterOperator.LessThanOrEqualTo },
        { label: "bevat", value: ELayerFilterOperator.ILike },
        { label: "bevat hoofdlettergevoelig", value: ELayerFilterOperator.Like },
        { label: "is leeg", value: ELayerFilterOperator.IsNull },
        { label: "is niet leeg", value: ELayerFilterOperator.IsNotNull },
      ],
    };
  },
  computed: {
    usesValueSelect() {
      return [ELayerFilterOperator.In, ELayerFilterOperator.NotIn].includes(this.selectedOperator);
    },
    usesTypedValue() {
      return ![
        ELayerFilterOperator.In,
        ELayerFilterOperator.NotIn,
        ELayerFilterOperator.IsNull,
        ELayerFilterOperator.IsNotNull,
      ].includes(this.selectedOperator);
    },
  },
  watch: {
    filterOptions(value) {
      this.currentFilterOptions = value;
    },
  },
  created() {
    this.store = useMapStore(this.mapId);

    this.setSelectedFilter(this.store.layerFilters[this.layerId]?.filters?.[this.filterProperty] || []);

    this.store.$subscribe((_, state) => {
      // From the moment this store subscription is created,
      // When the filters for the relevant layer change, the corresponding filter values
      // are updated to match the active filter values of the currently active filter.
      const filterValues = state.layerFilters[this.layerId]?.filters?.[this.filterProperty] || [];

      this.setSelectedFilter(filterValues);
    });
  },
  methods: {
    setSelectedFilter(filterValues) {
      if (Array.isArray(filterValues)) {
        this.selectedOperator = ELayerFilterOperator.In;
        this.selectedItems = filterValues;
        this.selectedValue = "";
        return;
      }

      this.selectedOperator = filterValues.operator;
      this.selectedItems = this.usesValueSelect ? filterValues.values : [];
      this.selectedValue = this.usesTypedValue ? filterValues.values[0] || "" : "";
    },
    updateFieldFilters() {
      if (this.usesValueSelect && this.selectedItems.length > 0) {
        this.$emit("onFilterChange", {
          ...this.fieldFilters,
          [this.filterProperty]: {
            operator: this.selectedOperator,
            values: this.selectedItems,
          },
        });
        return;
      }

      if (this.usesTypedValue && this.selectedValue.trim() !== "") {
        this.$emit("onFilterChange", {
          ...this.fieldFilters,
          [this.filterProperty]: {
            operator: this.selectedOperator,
            values: [this.selectedValue.trim()],
          },
        });
        return;
      }

      if ([ELayerFilterOperator.IsNull, ELayerFilterOperator.IsNotNull].includes(this.selectedOperator)) {
        this.$emit("onFilterChange", {
          ...this.fieldFilters,
          [this.filterProperty]: {
            operator: this.selectedOperator,
            values: [this.selectedOperator],
          },
        });
        return;
      }

      const newFieldFilter = {
        ...this.fieldFilters,
        [this.filterProperty]: {
          operator: this.selectedOperator,
          values: [],
        },
      };

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

.operator-select,
.filter-value-input {
  border: 1px solid var(--color-grey-60);
  border-radius: 6px;
  min-height: 38px;
  padding: 6px 8px;
  margin-bottom: 4px;
}

@media (max-width: 576px) {
  .filter-width {
    width: 100%;
    max-width: 100%;
  }
}
</style>
