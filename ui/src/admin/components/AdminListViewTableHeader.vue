<script setup lang="ts">
import ChevronDownIcon from "@/assets/icons/chevron-down-icon.svg";
import ChevronUpIcon from "@/assets/icons/chevron-up-icon.svg";
import { TableHeader } from "@/admin/components/AdminListViewTable.vue";

// Properties
type AdminListViewProps = {
  header: TableHeader;
  sort: TableHeaderRef;
};

const props = withDefaults(defineProps<AdminListViewProps>(), {});

// Emits
const emit = defineEmits<{
  (e: "update-list-sort", key: string): void;
}>();

// Table logic
export type TableHeaderRef = { sortKey: string; sortAscending: boolean };
</script>

<template>
  <button
    v-tippy="{ placement: 'bottom' }"
    aria-label="Sorteer kolom"
    content="Sorteer"
    class="tw-min-h-8"
    @click="
      () =>
        emit(
          'update-list-sort',
          props.header.overrideKeyForFilter ? props.header.overrideKeyForFilter : props.header.key,
        )
    "
  >
    <span class="tw-flex tw-flex-row tw-gap-1 tw-items-center">
      {{ props.header.header }}
      <span class="tw-mt-1">
        <ChevronUpIcon
          v-if="
            (props.header.overrideKeyForFilter
              ? props.header.overrideKeyForFilter === props.sort.sortKey
              : props.header.key === props.sort.sortKey) && props.sort.sortAscending
          "
        />
        <ChevronDownIcon
          v-if="
            (props.header.overrideKeyForFilter
              ? props.header.overrideKeyForFilter === props.sort.sortKey
              : props.header.key === props.sort.sortKey) && !props.sort.sortAscending
          "
        />
      </span>
    </span>
  </button>
</template>
