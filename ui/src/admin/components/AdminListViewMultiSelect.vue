<script setup lang="ts">
// Properties
import { TableFilter } from "@/admin/components/AdminListViewFilter.vue";
import { onMounted, ref, watch } from "vue";
import { useRoute } from "@/utils/inertia-routing";

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

let params: URLSearchParams = new URLSearchParams();

const multiselect = ref();

onMounted(() => {
  params = new URLSearchParams(route.query as any);

  const paramValue = params.get(props.filter.key);

  const selectedItems = paramValue ? paramValue.split(",") : [];

  const item = props.filter.options.filter((option: any) =>
    props.filter.dataKey
      ? selectedItems.includes(option[props.filter.dataKey].toString())
      : selectedItems.includes(option.toString()),
  );

  multiselect.value = item;
});

watch(multiselect, (value, oldValue) => {
  if (!oldValue) {
    return;
  }

  emit("update-list-filters", multiselect.value, props.filter.key);
});
</script>

<template>
  <multi-select
    v-model="multiselect"
    :options="filter.options"
    :option-label="filter.label"
    placeholder="Kies waarde"
    filter-placeholder="Zoek waarde"
    class="!tw-mt-0 !tw-text-sm md:!tw-max-w-48 md:!tw-min-w-48"
    filter
    :data-key="filter.dataKey"
  />
</template>
