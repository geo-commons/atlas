<script setup lang="ts">
// Properties
import { PageState } from "primevue/paginator";

type AdminListViewPaginatorProps = {
  totalResults: number;
  pagination: PaginationRef;
};

const props = withDefaults(defineProps<AdminListViewPaginatorProps>(), {});

// Emits
const emit = defineEmits<{
  (e: "update-list-pagination", pagination: PageState): void;
}>();

// Table logic
export type PaginationRef = {
  page: number;
  rows: number;
};
</script>

<template>
  <div class="tw-py-4 !tw-text-sm tw-flex tw-flex-col md:tw-flex-row tw-justify-between tw-items-center">
    <Paginator
      :rows="pagination.rows"
      :first="pagination.page * pagination.rows - 1 + pagination.rows"
      :total-records="totalResults"
      template="RowsPerPageDropdown FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
      :rows-per-page-options="[10, 15, 20, 30, 50, 100, 200, 500]"
      :pt="{
        root: {
          class: ['!tw-bg-transparent !tw-px-0 !tw-flex'],
        },
      }"
      @page="(pageState: PageState) => emit('update-list-pagination', pageState)"
    >
    </Paginator>
    <p class="tw-text-sm">Aantal resultaten: {{ props.totalResults }}</p>
  </div>
</template>
