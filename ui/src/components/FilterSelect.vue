<template>
  <div v-if="filterOptions && filterProperty" class="flex __column filter-width">
    <label :for="filterProperty" class="filter-label-padding">{{
      filterPropertyDisplayName ? filterPropertyDisplayName : filterProperty
    }}</label>
    <Select
      v-model="selectedOperator"
      :options="operatorOptions"
      option-label="label"
      option-value="value"
      class="filter-control"
      aria-label="Filtertype"
      @update:model-value="updateOperator"
    />
    <multi-select
      v-if="filterInputType === 'multi-select'"
      v-model="selectedValues"
      :options="currentFilterOptionsWithoutEmpty"
      option-label="label"
      option-value="value"
      :virtual-scroller-options="{ itemSize: 50 }"
      placeholder="Kies waarde"
      filter-placeholder="Zoek waarde"
      filter
      @update:model-value="updateFieldFilters()"
    />
    <Select
      v-else-if="filterInputType === 'select'"
      v-model="selectedSingleValue"
      :options="currentFilterOptionsWithoutEmpty"
      option-label="label"
      option-value="value"
      :virtual-scroller-options="{ itemSize: 50 }"
      placeholder="Kies waarde"
      filter-placeholder="Zoek waarde"
      filter
      class="filter-control"
      @update:model-value="updateFieldFilters()"
    />
    <InputNumber
      v-else-if="filterInputType === 'number'"
      v-model="selectedSingleValue"
      placeholder="Vul waarde in"
      class="filter-control"
      :max-fraction-digits="filterPropertyType === 'int' ? 0 : 16"
      @update:model-value="updateFieldFilters()"
    />
    <DatePicker
      v-else-if="filterInputType === 'temporal'"
      v-model="selectedSingleValue"
      :date-format="isTimeFilter ? undefined : 'dd-mm-yy'"
      :show-time="isDateTimeFilter"
      :time-only="isTimeFilter"
      placeholder="Kies datum"
      show-icon
      class="filter-control"
      @update:model-value="updateFieldFilters()"
    />
  </div>
</template>

<script>
import { useMapStore } from "@/stores/map_store";
import { EPanelFilterOperator } from "@/types/mapStore";
import { normalizeType, NUMERIC_TYPES, TEMPORAL_TYPES } from "@/utils/layer-filter-cql";
import { format, isValid, parseISO } from "date-fns";

const TEXT_OPERATOR_OPTIONS = [
  { label: "Gelijk", value: EPanelFilterOperator.Equals },
  { label: "Niet gelijk", value: EPanelFilterOperator.NotEquals },
  { label: "Leeg", value: EPanelFilterOperator.Empty },
  { label: "Niet leeg", value: EPanelFilterOperator.NotEmpty },
];

const NUMERIC_OPERATOR_OPTIONS = [
  { label: "Gelijk", value: EPanelFilterOperator.Equals },
  { label: "Niet gelijk", value: EPanelFilterOperator.NotEquals },
  { label: "Groter dan", value: EPanelFilterOperator.GreaterThan },
  { label: "Groter of gelijk", value: EPanelFilterOperator.GreaterThanOrEqual },
  { label: "Kleiner dan", value: EPanelFilterOperator.LessThan },
  { label: "Kleiner of gelijk", value: EPanelFilterOperator.LessThanOrEqual },
  { label: "Leeg", value: EPanelFilterOperator.Empty },
  { label: "Niet leeg", value: EPanelFilterOperator.NotEmpty },
];

const EMPTY_OPERATORS = [EPanelFilterOperator.Empty, EPanelFilterOperator.NotEmpty];

const FILTER_INPUT_TYPES = {
  MultiSelect: "multi-select",
  Number: "number",
  Select: "select",
  Temporal: "temporal",
};

export default {
  name: "FilterSelect",
  props: {
    filterOptions: Array,
    fieldFilters: Object,
    filterProperty: String,
    filterPropertyType: String,
    mapId: String,
    layerId: String,
    filterPropertyDisplayName: String,
  },
  emits: ["onFilterChange"],
  data() {
    return {
      selectedValues: [],
      selectedOperator: EPanelFilterOperator.Equals,
      selectedSingleValue: null,
      store: null,
    };
  },
  computed: {
    normalizedFilterPropertyType() {
      return normalizeType(this.filterPropertyType);
    },
    isNumericFilter() {
      return NUMERIC_TYPES.includes(this.normalizedFilterPropertyType);
    },
    isTemporalFilter() {
      return TEMPORAL_TYPES.includes(this.normalizedFilterPropertyType);
    },
    isDateTimeFilter() {
      return this.normalizedFilterPropertyType === "date-time";
    },
    isTimeFilter() {
      return this.normalizedFilterPropertyType === "time";
    },
    needsValue() {
      return !EMPTY_OPERATORS.includes(this.selectedOperator);
    },
    filterInputType() {
      if (!this.needsValue) {
        return null;
      }

      if (this.isNumericFilter) {
        return FILTER_INPUT_TYPES.Number;
      }

      if (this.isTemporalFilter) {
        return FILTER_INPUT_TYPES.Temporal;
      }

      if (this.selectedOperator === EPanelFilterOperator.Equals) {
        return FILTER_INPUT_TYPES.MultiSelect;
      }

      return FILTER_INPUT_TYPES.Select;
    },
    operatorOptions() {
      return this.isNumericFilter || this.isTemporalFilter ? NUMERIC_OPERATOR_OPTIONS : TEXT_OPERATOR_OPTIONS;
    },
    currentFilterOptions() {
      return this.filterOptions.map((filterOption) => ({
        label: String(filterOption),
        value: filterOption,
      }));
    },
    currentFilterOptionsWithoutEmpty() {
      return this.currentFilterOptions.filter((filterOption) => filterOption.value !== "Leeg");
    },
  },
  created() {
    this.store = useMapStore(this.mapId);

    const filterValue = this.store.layerFilters[this.layerId]?.filters?.[this.filterProperty];

    if (filterValue) {
      this.selectedOperator = filterValue.operator;
      this.selectedValues = filterValue.values || [];
      this.selectedSingleValue = this.isTemporalFilter
        ? this.parseTemporalValue(filterValue.values?.[0])
        : (filterValue.values?.[0] ?? null);
    }

    this.store.$subscribe((_, state) => {
      if (!state.layerFilters[this.layerId]?.filters?.[this.filterProperty]) {
        this.resetLocalFilter();
      }
    });
  },
  methods: {
    resetLocalFilter() {
      this.selectedOperator = EPanelFilterOperator.Equals;
      this.selectedValues = [];
      this.selectedSingleValue = null;
    },
    updateOperator() {
      this.selectedValues = [];
      this.selectedSingleValue = null;
      this.updateFieldFilters();
    },
    updateFieldFilters() {
      this.$emit("onFilterChange", {
        ...this.fieldFilters,
        [this.filterProperty]: {
          operator: this.selectedOperator,
          values: this.getSelectedFilterValues(),
          type: this.filterPropertyType,
        },
      });
    },
    getSelectedFilterValues() {
      if (!this.needsValue) {
        return [];
      }

      if (this.filterInputType === FILTER_INPUT_TYPES.MultiSelect) {
        return this.selectedValues;
      }

      if (this.selectedSingleValue === null || this.selectedSingleValue === "") {
        return [];
      }

      const selectedValue = this.isTemporalFilter
        ? this.formatTemporalFilterValue(this.selectedSingleValue)
        : this.selectedSingleValue;

      return selectedValue === null || selectedValue === "" ? [] : [selectedValue];
    },
    parseTemporalValue(value) {
      if (!value) {
        return null;
      }

      if (value instanceof Date) {
        return isValid(value) ? value : null;
      }

      if (this.isTimeFilter && /^\d{2}:\d{2}(:\d{2})?$/.test(String(value))) {
        const [hours, minutes, seconds = "0"] = String(value).split(":");
        const date = new Date();
        date.setHours(Number(hours), Number(minutes), Number(seconds), 0);

        return isValid(date) ? date : null;
      }

      const date = parseISO(
        String(value)
          .replace(/Z$/, "")
          .replace(/\.\d+$/, ""),
      );

      return isValid(date) ? date : null;
    },
    formatTemporalFilterValue(value) {
      const date = this.parseTemporalValue(value);

      if (!date) {
        return null;
      }

      if (this.normalizedFilterPropertyType === "date") {
        return format(date, "yyyy-MM-dd");
      }

      if (this.normalizedFilterPropertyType === "time") {
        return format(date, "HH:mm:ss");
      }

      return format(date, "yyyy-MM-dd'T'HH:mm:ss");
    },
  },
};
</script>
<style scoped>
.filter-width {
  min-width: 125px;
  max-width: 225px;
  gap: 8px;
}

.filter-control {
  width: 100%;
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
