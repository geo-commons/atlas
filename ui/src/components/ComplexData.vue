<template>
  <div class="tw-mb-4">
    <DataTable
      v-if="isComplexArray(dataValue) || valueType === 'OBJECT'"
      :value="tableValue"
      size="small"
      scrollable
      scroll-height="260px"
      responsive-layout="scroll"
      class="tw-w-full"
    >
      <Column v-for="col in objectTableColumns" :key="col" :field="col" :header="prettyHeader(col)">
        <template #body="{ data }">
          <RichValue :data-key="col" :data-value="data?.[col]" :position="position" />
        </template>
      </Column>

      <template #empty>
        <span class="tw-text-gray-400">Geen items</span>
      </template>
    </DataTable>

    <div v-else-if="isSimpleArray(dataValue)" class="tw-mb-4">
      <ul class="tw-list-disc tw-ml-5 tw-space-y-1">
        <li v-for="(item, i) in dataValue" :key="i" class="tw-break-words">
          <RichValue :data-key="String(i)" :data-value="item" :position="position" />
        </li>
      </ul>
    </div>

    <div v-else class="tw-mb-4">Kan de waarde niet weergeven. Ongeldig formaat.</div>
  </div>
</template>

<script setup>
import { computed } from "vue";
import DataTable from "primevue/datatable";
import Column from "primevue/column";
import RichValue from "./RichValue.vue";
import { formatRawString } from "@/utils/string-helpers";

const props = defineProps({
  dataValue: {
    type: [String, Number, Object, Array, Boolean, null],
    default: null,
  },
  valueType: {
    type: String,
    required: true,
  },
  position: {
    type: String,
    default: "right",
  },
});

const tableValue = computed(() => {
  return props.valueType === "OBJECT" ? [props.dataValue] : props.dataValue;
});

const objectTableColumns = computed(() => {
  if (props.valueType === "OBJECT" && isPlainObject(props.dataValue)) {
    return Object.keys(props.dataValue);
  }

  if (!Array.isArray(props.dataValue)) {
    return [];
  }

  const sample = props.dataValue.slice(0, 50).filter((item) => isPlainObject(item));

  const keys = new Set();

  for (const row of sample) {
    Object.keys(row).forEach((key) => keys.add(key));
  }

  return Array.from(keys);
});

const prettyHeader = (key) => {
  return formatRawString(key);
};

const isSimpleArray = (value) => {
  return Array.isArray(value) && value.length > 0 && (typeof value[0] !== "object" || value[0] === null);
};

const isComplexArray = (value) => {
  return Array.isArray(value) && value.length > 0 && isPlainObject(value[0]);
};

const isPlainObject = (value) => {
  return value !== null && typeof value === "object" && !Array.isArray(value);
};
</script>
