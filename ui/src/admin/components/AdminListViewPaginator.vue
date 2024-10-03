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
  <div class="tw-py-4 !tw-text-sm">
    <Paginator
      :rows="pagination.rows"
      :first="(pagination.page - 1) * pagination.rows + 1"
      :total-records="totalResults"
      template="RowsPerPageDropdown FirstPageLink PrevPageLink PageLinks NextPageLink LastPageLink"
      :rows-per-page-options="[10, 15, 20, 30, 50, 100, 200, 500]"
      :pt="{
        paginatorContainer: {
          class: [''],
        },
        root: {
          class: ['!tw-bg-transparent !tw-px-0'],
        },
        page: {
          class: [''],
        },
      }"
      @page="(pageState: PageState) => $emit('update-list-pagination', pageState)"
    >
      <template #end>
        <p class="tw-text-sm">Aantal resultaten: {{ props.totalResults }}</p>
      </template>
    </Paginator>
  </div>
</template>
