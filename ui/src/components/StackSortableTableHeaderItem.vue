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
        <ChevronUpIcon v-if="getSortStack && getSortStack.asc" class="icon __smedium" />
        <ChevronDownIcon v-if="getSortStack && !getSortStack.asc" class="icon __smedium" />
      </span>
    </span>
  </button>
</template>

<script>
import ChevronDownIcon from "../assets/icons/chevron-down-icon.svg";
import ChevronUpIcon from "../assets/icons/chevron-up-icon.svg";

export default {
  name: "StackSortableTableHeaderItem",
  components: {
    ChevronUpIcon,
    ChevronDownIcon,
  },
  props: {
    headerText: String,
    property: String,
    sortStack: Array,
  },
  computed: {
    getSortStack() {
      const result = this.sortStack.filter((value) => value.id === this.property);

      return result.length > 0 ? result[0] : null;
    },
  },
  methods: {
    sortColumn() {
      let ascending = null;
      /* if sortAscending is null, we want it to move it to true.
      If its true we want to move it to false, and if its false we want to move it to null.
      When it is set to null the sorting for this property is removed */
      if (this.getSortStack === null) {
        ascending = true;
      } else if (this.getSortStack.asc === true) {
        ascending = false;
      } else {
        ascending = null;
      }

      this.$emit("sort", this.property, ascending);
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
