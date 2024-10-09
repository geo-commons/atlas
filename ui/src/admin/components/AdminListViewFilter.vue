<script setup lang="ts">
import { onMounted, ref, Ref } from "vue";
import AdminListViewMultiSelect from "@/admin/components/AdminListViewMultiSelect.vue";

// Properties
type AdminListViewFilterProps = {
  params: URLSearchParams;
  singularName: string;
  getTableFilters?: () => Array<TableFilter>;
};

const props = withDefaults(defineProps<AdminListViewFilterProps>(), {});

// Emits
const emit = defineEmits<{
  (e: "update-search-term", value: string): void;
  (e: "update-list-filters", value: any, key: string): void;
}>();

// Table logic
export type TableFilter = {
  name: string;
  key: string;
  options: any;
  label: string;
  dataKey?: string;
};

const tableFilters: Ref<Array<TableFilter>> = ref([]);

// Lifecycle hooks
onMounted(async () => {
  if (props.getTableFilters) {
    tableFilters.value = props.getTableFilters();
  }
});
</script>

<template>
  <div class="tw-pb-4 tw-flex tw-flex-col md:tw-flex-row md:tw-justify-between md:tw-items-end tw-gap-2">
    <InputGroup class="!tw-w-full md:!tw-w-1/4">
      <InputGroupAddon>
        <i class="pi pi-search !tw-h-4 !tw-w-4"></i>
      </InputGroupAddon>
      <InputText
        :model-value="props.params.get('search')"
        class="!tw-text-sm"
        :placeholder="'Zoek op ' + props.singularName.toLowerCase()"
        @update:modelValue="(value: string) => $emit('update-search-term', value)"
      />
    </InputGroup>
    <div class="tw-flex tw-flex-col md:tw-flex-row tw-gap-2 tw-max-w-full">
      <div v-for="filter in tableFilters" :key="filter.key" class="tw-flex tw-flex-col tw-gap-1">
        <span class="tw-font-medium tw-text-sm">{{ filter.name }}</span>
        <AdminListViewMultiSelect
          :filter="filter"
          @update-list-filters="(value: any, key: string) => $emit('update-list-filters', value, key)"
        />
      </div>
    </div>
  </div>
</template>
