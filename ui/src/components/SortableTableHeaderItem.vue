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
      <span class="icon-min-width">
        <ArrowUpIcon v-if="property === sortKey && sortAscending" />
        <ArrowDownIcon v-if="property === sortKey && !sortAscending" />
      </span>
    </span>
  </button>
</template>

<script>
import ArrowDownIcon from "../icons/ArrowDownIcon.vue";
import ArrowUpIcon from "../icons/ArrowUpIcon.vue";

export default {
  name: "SortableTableHeaderItem",
  components: {
    ArrowUpIcon,
    ArrowDownIcon,
  },
  props: {
    headerText: String,
    property: String,
    sortKey: String,
    sortAscending: Boolean,
  },
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
  gap: 3px;
  text-transform: capitalize;
  justify-content: flex-start;
}

.icon-min-width {
  min-width: 24px;
}
</style>
