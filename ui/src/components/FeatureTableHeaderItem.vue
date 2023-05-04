<template>
  <div class="flex flex-column">
    <div class="table-header-container">
      <span @click="() => sortColumn()" class="header-text">
        {{ headerText }}
      </span>
      <button
        @click="() => sortColumn()"
        aria-label="Sorteer kolom"
        v-tippy="{ placement: 'bottom' }"
        content="Sorteer"
      >
        <SortIcon v-if="property !== sortKey" />
        <ArrowUpIcon v-if="property === sortKey && sortAscending" />
        <ArrowDownIcon v-if="property === sortKey && !sortAscending" />
      </button>
      <FilterTooltip
        :layer="layer"
        :property="property"
        :fieldFilters="fieldFilters"
        @change="(value) => updateFilter(value)"
      />
    </div>
    <div class="flex">
      {{ fieldFilters && fieldFilters[property] ? fieldFilters[property] : "" }}
      <button
        v-if="fieldFilters && fieldFilters[property]"
        class="iconbutton"
        aria-label="Verwijder filter"
        v-tippy="{ placement: 'bottom' }"
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
  data() {
    return {
      test: {},
    };
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
  display: flex;
  font-weight: 500;
  gap: 3px;
  text-transform: capitalize;
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
