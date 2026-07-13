<script setup lang="ts">
// Properties
import { TableFilter } from "@/admin/components/AdminListViewFilter.vue";
import { ref, watch } from "vue";
import { useRoute } from "vue-router";

type AdminListViewFilterProps = {
  filter: TableFilter;
};

const props = withDefaults(defineProps<AdminListViewFilterProps>(), {});

// Emits
const emit = defineEmits<{
  (e: "update-list-filters", value: any, key: string): void;
}>();

// Multiselect logic
const route = useRoute();

const multiselect = ref();

const updateMultiselectState = () => {
  const params = new URLSearchParams(route.query as any);

  const paramValue = params.get(props.filter.key);
  const selectedItems = paramValue ? paramValue.split(",") : [];

  const item = props.filter.options.filter((option: any) =>
    props.filter.dataKey
      ? selectedItems.includes(option[props.filter.dataKey].toString())
      : selectedItems.includes(option.toString()),
  );

  multiselect.value = item;
};

const updateListFilter = (value: any) => {
  multiselect.value = value;
  emit("update-list-filters", value, props.filter.key);
};

watch(
  () => [route.query, props.filter.options],
  () => {
    updateMultiselectState();
  },
  { immediate: true, deep: true },
);
</script>

<template>
  <multi-select
    :model-value="multiselect"
    :options="filter.options"
    :option-label="filter.label"
    placeholder="Kies waarde"
    filter-placeholder="Zoek waarde"
    class="!tw-mt-0 !tw-text-sm md:!tw-max-w-48 md:!tw-min-w-48"
    filter
    :data-key="filter.dataKey"
    @update:model-value="updateListFilter"
  />
</template>
