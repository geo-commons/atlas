<template>
  <button
    v-tippy="{ placement: 'bottom' }"
    :aria-label="ariaLabel"
    :content="tooltipContent"
    aria-live="assertive"
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

<script setup>
import { computed } from "vue";
import ChevronDownIcon from "../assets/icons/chevron-down-icon.svg";
import ChevronUpIcon from "../assets/icons/chevron-up-icon.svg";

const props = defineProps({
  headerText: String,
  property: String,
  sortStack: Array,
});

const emit = defineEmits(["sort"]);

const getSortStack = computed(() => {
  const result = props.sortStack.filter((value) => value.id === props.property);
  return result.length > 0 ? result[0] : null;
});

const getSortActionText = () => {
  if (getSortStack.value === null) {
    return "Sorteer oplopend";
  } else if (getSortStack.value.asc === true) {
    return "Sorteer aflopend";
  } else {
    return "Verwijder sortering";
  }
};

const tooltipContent = computed(() => {
  return getSortActionText();
});

const ariaLabel = computed(() => {
  const headerName = props.headerText || "Kolom";
  return `${headerName}, ${getSortActionText()}`;
});

const sortColumn = () => {
  let ascending = null;
  /* if sortAscending is null, we want it to move it to true.
  If its true we want to move it to false, and if its false we want to move it to null.
  When it is set to null the sorting for this property is removed */
  if (getSortStack.value === null) {
    ascending = true;
  } else if (getSortStack.value.asc === true) {
    ascending = false;
  } else {
    ascending = null;
  }

  emit("sort", props.property, ascending);
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
