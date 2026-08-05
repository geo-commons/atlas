<template>
  <MultiSelect
    :model-value="modelValue"
    placeholder="Kies kaarten"
    filter-placeholder="Zoek kaart"
    :options="options"
    :disabled="disabled"
    option-label="label"
    option-value="value"
    display="chip"
    filter
    fluid
    :pt="{
      root: '!tw-mt-2 tw-max-w-full md:tw-max-w-[426px]',
      overlay: 'tw-max-w-full md:tw-max-w-[426px]',
      labelContainer: 'tw-w-full tw-min-w-0',
      label:
        'tw-flex tw-flex-wrap tw-items-center tw-gap-1 tw-min-h-10 tw-py-2 tw-pl-3 tw-pr-8 tw-overflow-hidden tw-w-full tw-max-w-full',
      option: 'tw-overflow-hidden tw-max-w-full',
      optionContent: 'tw-max-w-full tw-overflow-hidden',
    }"
    @update:model-value="handleModelValueUpdate"
  >
    <template #option="{ option }">
      <div class="tw-py-2 tw-w-full tw-min-w-0">
        <div
          class="tw-font-semibold tw-text-sm tw-overflow-hidden tw-whitespace-nowrap tw-text-ellipsis tw-w-full tw-min-w-0"
        >
          {{ option.label }}
        </div>
        <div
          v-if="option.slug"
          class="tw-text-xs tw-text-gray-500 tw-mt-0.5 tw-overflow-hidden tw-whitespace-nowrap tw-text-ellipsis tw-w-full tw-min-w-0"
        >
          {{ option.slug }}
        </div>
      </div>
    </template>
    <template #empty>
      <span class="tw-text-sm tw-text-gray-500">Er zijn geen kaarten beschikbaar.</span>
    </template>
    <template #emptyfilter>
      <span class="tw-text-sm tw-text-gray-500">Geen kaarten gevonden.</span>
    </template>
  </MultiSelect>
</template>

<script setup lang="ts">
interface IMapOption {
  label: string;
  value: number;
  slug?: string;
}

interface IMapsFieldProps {
  modelValue?: number[];
  options?: IMapOption[];
  disabled?: boolean;
}

type MapsFieldValue = Array<number | string> | null;

const { modelValue = [], options = [], disabled = false } = defineProps<IMapsFieldProps>();

const emit = defineEmits<{
  "update:modelValue": [value: number[]];
}>();

const handleModelValueUpdate = (value: MapsFieldValue): void => {
  emit(
    "update:modelValue",
    (value || []).map((mapId) => Number(mapId)),
  );
};
</script>

<style scoped>
.p-multiselect {
  max-width: 100vw;
}
</style>
