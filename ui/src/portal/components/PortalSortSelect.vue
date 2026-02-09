<template>
  <div class="tw-flex tw-items-center tw-gap-2">
    <Dropdown
      v-model="selectedSort"
      :options="sortOptions"
      option-label="label"
      option-value="value"
      class="tw-w-full"
    />
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";

interface SortOption {
  value: string;
  label: string;
}

interface PortalSortSelectProps {
  selectedSort?: string;
}

interface PortalSortSelectEmits {
  (e: "on-sort-change", value: string): void;
}

const props = withDefaults(defineProps<PortalSortSelectProps>(), {
  selectedSort: "title",
});

const emit = defineEmits<PortalSortSelectEmits>();

const sortOptions: SortOption[] = [
  { value: "title", label: "Titel (A-Z)" },
  { value: "-title", label: "Titel (Z-A)" },
  { value: "-last_updated", label: "Laatst bijgewerkt (nieuwste eerst)" },
  { value: "last_updated", label: "Laatst bijgewerkt (oudste eerst)" },
];

const selectedSort = computed({
  get: () => props.selectedSort,
  set: (value: string) => emit("on-sort-change", value),
});
</script>
