<template>
  <button
    v-tippy="{ placement: 'bottom' }"
    aria-label="Sorteer kolom"
    content="Sorteer"
    class="header-background"
    @click="() => sortColumn()"
  >
    <span class="table-header-container">
      {{ headerText }}
      <span class="flex __center icon-min-width">
        <ChevronUpIcon v-if="property === sortKey && sortAscending" class="icon __smedium" />
        <ChevronDownIcon v-if="property === sortKey && !sortAscending" class="icon __smedium" />
      </span>
    </span>
  </button>
</template>

<script>
import ChevronDownIcon from "../assets/icons/chevron-down-icon.svg";
import ChevronUpIcon from "../assets/icons/chevron-up-icon.svg";

export default {
  name: "SortableTableHeaderItem",
  components: {
    ChevronUpIcon,
    ChevronDownIcon,
  },
  props: {
    headerText: String,
    property: String,
    sortKey: String,
    sortAscending: Boolean,
  },
  emits: ["sort"],
  methods: {
    sortColumn() {
      this.$emit("sort", this.property);
    },
  },
};
</script>

<style scoped>
.header-background {
  background: inherit;
}

.table-header-container {
  display: flex;
  font-weight: var(--font-weight-normal);
  text-transform: capitalize;
  justify-content: flex-start;
}

.icon-min-width {
  min-width: 18px;
}
</style>
