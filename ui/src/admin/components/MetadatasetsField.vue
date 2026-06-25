<template>
  <div class="metadatasets-field">
    <Select
      :model-value="modelValue"
      placeholder="Kies een metadataset"
      filter-placeholder="Zoek metadataset"
      :options="options"
      :loading="false"
      option-label="label"
      option-value="value"
      filter
      fluid
      :pt="{
        root: '!tw-mt-2 tw-max-w-full md:tw-max-w-[426px]',
        overlay: 'tw-max-w-full md:tw-max-w-[426px]',
        input: 'tw-overflow-hidden tw-whitespace-nowrap tw-text-ellipsis tw-max-w-full',
        value: 'tw-overflow-hidden tw-whitespace-nowrap tw-text-ellipsis tw-w-full tw-max-w-full',
        option: 'tw-overflow-hidden tw-max-w-full',
        optionContent: 'tw-max-w-full tw-overflow-hidden',
      }"
      @update:model-value="handleModelValueUpdate"
    >
      <template #option="{ option }">
        <div class="tw-py-2 tw-w-full tw-min-w-0">
          <div
            class="tw-font-semibold tw-text-sm tw-mb-1 tw-overflow-hidden tw-whitespace-nowrap tw-text-ellipsis tw-w-full tw-min-w-0"
          >
            {{ option.label }}
          </div>
          <div
            v-if="option.organization"
            class="tw-text-xs tw-text-gray-600 tw-mb-0.5 tw-overflow-hidden tw-whitespace-nowrap tw-text-ellipsis tw-w-full tw-min-w-0"
          >
            {{ option.organization }}
          </div>
          <div
            v-if="option.last_updated"
            class="tw-text-xs tw-text-gray-500 tw-mb-1 tw-overflow-hidden tw-whitespace-nowrap tw-text-ellipsis tw-w-full tw-min-w-0"
          >
            Laatst bijgewerkt: {{ formatDate(option.last_updated) }}
          </div>
          <div
            v-if="option.description"
            class="tw-text-xs tw-text-gray-700 tw-leading-relaxed tw-w-full tw-overflow-hidden tw-whitespace-nowrap tw-text-ellipsis tw-min-w-0"
          >
            {{ option.description }}
          </div>
        </div>
      </template>
      <template #footer>
        <div class="tw-w-full tw-border-0 tw-border-t-[1px] tw-border-gray-200 tw-border-solid">
          <router-link
            to="/metadatasets/"
            class="tw-flex tw-gap-2 tw-items-center tw-justify-center tw-no-underline tw-text-sm tw-font-medium tw-text-gray-700 tw-text-center tw-w-full !tw-hover:tw-bg-gray-50 tw-rounded-md tw-bg-white tw-p-3"
            target="_blank"
          >
            <i class="pi pi-plus tw-text-gray-400"></i>
            Nieuwe metadataset toevoegen
          </router-link>
        </div>
      </template>
      <template #value>
        <div class="tw-flex tw-items-center tw-justify-between tw-w-full tw-min-w-0">
          <span class="tw-overflow-hidden tw-whitespace-nowrap tw-text-ellipsis tw-flex-1 tw-min-w-0">{{
            selectedMetadataset?.label || "Kies een metadataset"
          }}</span>
          <button
            v-if="modelValue !== null && modelValue !== undefined"
            type="button"
            class="tw-ml-2 tw-p-1 tw-text-gray-400 hover:tw-text-gray-600 focus:tw-outline-none tw-flex-shrink-0"
            title="Verwijder geselecteerde metadataset"
            @click.stop="clearSelection"
          >
            <i class="pi pi-times tw-w-3 tw-h-3"></i>
          </button>
        </div>
      </template>
    </Select>

    <!-- Selected dataset information -->
    <div v-if="selectedMetadataset" class="tw-mt-4 tw-bg-white tw-rounded-lg tw-border tw-border-gray-200 tw-p-4">
      <div class="tw-space-y-3">
        <div v-if="selectedMetadataset.description" class="tw-flex tw-flex-col">
          <span class="tw-text-sm tw-text-gray-500 tw-mb-1">Toelichting</span>
          <span class="tw-text-sm tw-font-medium tw-text-gray-900">{{ selectedMetadataset.description }}</span>
        </div>

        <div v-if="selectedMetadataset.organization" class="tw-flex tw-flex-col">
          <span class="tw-text-sm tw-text-gray-500 tw-mb-1">Bronleverancier</span>
          <span class="tw-text-sm tw-font-medium tw-text-gray-900">{{ selectedMetadataset.organization }}</span>
        </div>

        <div
          v-if="selectedMetadataset.last_updated || selectedMetadataset.update_frequency"
          class="tw-flex tw-flex-row tw-gap-6 tw-flex-wrap"
        >
          <div v-if="selectedMetadataset.last_updated" class="tw-flex tw-flex-col">
            <span class="tw-text-sm tw-text-gray-500 tw-mb-1">Laatst bijgewerkt</span>
            <span class="tw-text-sm tw-font-medium tw-text-gray-900">{{
              formatDate(selectedMetadataset.last_updated)
            }}</span>
          </div>

          <div v-if="selectedMetadataset.update_frequency" class="tw-flex tw-flex-col">
            <span class="tw-text-sm tw-text-gray-500 tw-mb-1">Updatefrequentie</span>
            <span class="tw-text-sm tw-font-medium tw-text-gray-900">{{ selectedMetadataset.update_frequency }}</span>
          </div>
        </div>

        <div v-if="selectedMetadataset.responsible_email_internal" class="tw-flex tw-flex-col">
          <span class="tw-text-sm tw-text-gray-500 tw-mb-1">Aanspreekpunt intern</span>
          <span class="tw-text-sm tw-font-medium tw-text-gray-900">{{
            selectedMetadataset.responsible_email_internal
          }}</span>
        </div>
      </div>

      <div class="tw-mt-4 tw-pt-3 tw-border-t tw-border-gray-200">
        <router-link
          class="tw-inline-flex tw-items-center tw-gap-2 tw-px-4 tw-py-2 tw-bg-white tw-border tw-border-gray-300 tw-rounded-md tw-text-sm tw-font-medium tw-text-gray-700 hover:tw-bg-gray-50 focus:tw-outline-none focus:tw-ring-2 focus:tw-ring-offset-2 focus:tw-ring-blue-500 tw-border-solid tw-no-underline"
          :to="`/metadatasets/update/${selectedMetadataset.id}`"
          target="_blank"
          rel="noopener"
        >
          <i class="pi pi-external-link tw-w-4 tw-h-4 tw-text-gray-400"></i>
          Bekijk volledige metadataset
        </router-link>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { IMetadatasetOption } from "@/types/metadataset";
import { computed, type ComputedRef, toRefs } from "vue";
import { formatDateValue } from "../../utils/date-formatter";

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
  const found = options.value.find((metadataset) => metadataset.value === modelValue.value);
  return found || null;
});

const handleModelValueUpdate = (value: string | number | null): void => {
  const processedValue = value ? Number(value) : null;
  emit("update:modelValue", processedValue);
};

const formatDate = (dateString: string): string => {
  if (!dateString) return "";
  return formatDateValue(dateString, {
    year: "numeric",
    month: "long",
    day: "numeric",
  } as any);
};

const clearSelection = (): void => {
  emit("update:modelValue", null);
};
</script>

<style scoped>
.p-select {
  max-width: 100vw;
}
</style>
