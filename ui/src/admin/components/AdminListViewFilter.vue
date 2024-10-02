<script setup lang="ts">
// Properties
type AdminListViewFilterProps = {
  params: URLSearchParams;
};

const props = withDefaults(defineProps<AdminListViewFilterProps>(), {});

// Emits
const emit = defineEmits<{
  (e: "update-search-term", value: string): void;
}>();
</script>

<template>
  <div class="tw-pb-4">
    <InputGroup class="!tw-w-full md:!tw-w-1/4">
      <InputGroupAddon>
        <i class="pi pi-search !tw-h-4 !tw-w-4"></i>
      </InputGroupAddon>
      <InputText
        :model-value="props.params.get('search')"
        class="!tw-text-sm"
        placeholder="Zoekterm..."
        @update:modelValue="(value: string) => $emit('update-search-term', value)"
      />
    </InputGroup>
  </div>
</template>
