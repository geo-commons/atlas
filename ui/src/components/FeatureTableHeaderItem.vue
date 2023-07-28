<template>
  <div class="flex flex-column">
    <div class="flex-center table-header-container">
      <span class="header-text" @click="() => sortColumn()">
        {{ headerText }}
      </span>
      <button
        v-tippy="{ placement: 'bottom' }"
        aria-label="Sorteer kolom"
        content="Sorteer"
        class="flex-center"
        @click="() => sortColumn()"
      >
        <SortIcon v-if="property !== sortKey" />
        <ArrowUpIcon v-if="property === sortKey && sortAscending" />
        <ArrowDownIcon v-if="property === sortKey && !sortAscending" />
      </button>
      <FilterTooltip
        :layer="layer"
        :property="property"
        :field-filters="fieldFilters"
        @change="(value) => updateFilter(value)"
      />
    </div>
    <div class="flex">
      {{ fieldFilters && fieldFilters[property] ? fieldFilters[property] : "" }}
      <button
        v-if="fieldFilters && fieldFilters[property]"
        v-tippy="{ placement: 'bottom' }"
        class="iconbutton"
        aria-label="Verwijder filter"
        content="Verwijder"
        @click="() => removeFilter()"
      >
        <CloseIcon />
      </button>
    </div>
  </div>
</template>

<script>
import ArrowDownIcon from "../icons/ArrowDownIcon.vue";
import ArrowUpIcon from "../icons/ArrowUpIcon.vue";
import CloseIcon from "../icons/CloseIcon.vue";
import FilterTooltip from "./FilterTooltip.vue";
import SortIcon from "../icons/SortIcon.vue";

export default {
  name: "FeatureTableHeaderItem",
  components: {
    FilterTooltip,
    CloseIcon,
    ArrowUpIcon,
    ArrowDownIcon,
    SortIcon,
  },
  props: {
    layer: Object,
    property: String,
    fieldFilters: Object,
    sortKey: String,
    sortAscending: Boolean,
  },
  computed: {
    headerText() {
      return this.layer.friendly_fields &&
        this.layer.friendly_fields[this.property]
        ? this.layer.friendly_fields[this.property]
        : this.property;
    },
  },
  methods: {
    updateFilter(filter) {
      this.$emit("change", filter);
    },
    removeFilter() {
      const newFieldFilter = { ...this.fieldFilters };
      delete newFieldFilter[this.property];
      this.$emit("change", newFieldFilter);
    },
    sortColumn() {
      this.$emit("sort", this.property);
    },
  },
};
</script>

<style scoped>
.table-header-container {
  font-weight: 500;
  gap: 3px;
  text-transform: capitalize;
}

.flex-center {
  display: flex;
  align-items: center;
}

.header-text {
  cursor: pointer;
}

.flex {
  display: flex;
}

.flex-column {
  flex-direction: column;
}
</style>
