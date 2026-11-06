<template>
  <div class="metadatasets-field tw-flex tw-w-full tw-items-stretch tw-gap-2">
    <Select
      :model-value="modelValue"
      placeholder="Kies een metadataset"
      filter-placeholder="Zoek metadataset"
      :options="options"
      :loading="false"
      option-label="label"
      option-value="value"
      class="tw-min-w-0 tw-flex-1"
      filter
      fluid
      show-clear
      :pt="{
        overlay: 'tw-max-w-full',
        input: 'tw-overflow-hidden tw-whitespace-nowrap tw-text-ellipsis tw-max-w-full',
        value: 'tw-overflow-hidden tw-whitespace-nowrap tw-text-ellipsis tw-w-full tw-max-w-full',
        option: 'tw-overflow-hidden tw-max-w-full',
        optionContent: 'tw-max-w-full tw-overflow-hidden',
      }"
      @update:model-value="handleModelValueUpdate"
    >
      <template #option="{ option }">
        <div class="tw-w-full tw-min-w-0 tw-py-2">
          <div
            class="tw-mb-1 tw-w-full tw-min-w-0 tw-overflow-hidden tw-text-ellipsis tw-whitespace-nowrap tw-text-sm tw-font-semibold"
          >
            {{ option.label }}
          </div>
          <div
            v-if="option.organization"
            class="tw-mb-0.5 tw-w-full tw-min-w-0 tw-overflow-hidden tw-text-ellipsis tw-whitespace-nowrap tw-text-xs tw-text-gray-600"
          >
            {{ option.organization }}
          </div>
          <div
            v-if="option.last_updated"
            class="tw-mb-1 tw-w-full tw-min-w-0 tw-overflow-hidden tw-text-ellipsis tw-whitespace-nowrap tw-text-xs tw-text-gray-500"
          >
            Laatst bijgewerkt: {{ formatDate(option.last_updated) }}
          </div>
          <div
            v-if="option.description"
            class="tw-w-full tw-overflow-hidden tw-text-ellipsis tw-whitespace-nowrap tw-text-xs tw-leading-relaxed tw-text-gray-700"
          >
            {{ option.description }}
          </div>
        </div>
      </template>
      <template #footer>
        <div class="tw-w-full tw-border-0 tw-border-t-[1px] tw-border-solid tw-border-gray-200">
          <router-link
            to="/metadatasets/"
            class="tw-flex tw-w-full tw-items-center tw-justify-center tw-gap-2 tw-rounded-md tw-bg-white tw-p-3 tw-text-center tw-text-sm tw-font-medium tw-text-gray-700 tw-no-underline hover:tw-bg-gray-50"
            target="_blank"
          >
            <i class="pi pi-plus tw-text-gray-400" />
            Nieuwe metadataset toevoegen
          </router-link>
        </div>
      </template>
    </Select>
    <router-link
      v-if="selectedMetadataset"
      v-slot="{ href }"
      custom
      :to="`/metadatasets/update/${selectedMetadataset.id}`"
    >
      <Button
        as="a"
        :href="href"
        target="_blank"
        rel="noopener"
        label="Bekijk"
        icon="pi pi-external-link"
        severity="secondary"
        outlined
        class="!tw-no-underline"
        aria-label="Open geselecteerde metadataset in een nieuw tabblad"
      />
    </router-link>
  </div>
</template>

<script setup lang="ts">
import { computed, type ComputedRef, toRefs } from "vue";
import { IMetadatasetOption } from "@/types/metadataset";
import { formatDateValue } from "@/utils/date-formatter";

interface MetadatasetsFieldProps {
  modelValue?: number | null;
  options?: IMetadatasetOption[];
}

interface Emits {
  "update:modelValue": [value: number | null];
}

const props = withDefaults(defineProps<MetadatasetsFieldProps>(), {
  modelValue: null,
  options: () => [],
});

const { modelValue, options } = toRefs(props);
const emit = defineEmits<Emits>();

const selectedMetadataset: ComputedRef<IMetadatasetOption | null> = computed(() => {
  if (!modelValue.value && modelValue.value !== 0) {
    return null;
  }

  return options.value.find((metadataset) => metadataset.value === modelValue.value) || null;
});

const handleModelValueUpdate = (value: string | number | null): void => {
  emit("update:modelValue", value ? Number(value) : null);
};

const formatDate = (dateString: string): string => {
  return formatDateValue(dateString, {
    year: "numeric",
    month: "long",
    day: "numeric",
  });
};
</script>

<style scoped>
.p-select {
  max-width: 100vw;
}
</style>
