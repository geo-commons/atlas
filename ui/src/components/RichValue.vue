<template>
  <div>
    <span v-if="valueType === 'NUMBER'">{{ dataValue }}</span>
    <span v-if="valueType === 'UNKNOWN'">{{ dataValue }}</span>
    <span v-if="valueType === 'DATE'">{{ friendlyDate(dataValue) }}</span>
    <markdown v-if="valueType === 'STRING'" :source="dataValue" />
    <a v-if="valueType === 'URL'" :href="normalizeUrlValue(dataValue)" target="_blank" rel="noopener">{{
      dataValue.length >= 75
        ? `${dataValue.substring(0, 36)}...${dataValue.substring(dataValue.length - 36)}`
        : dataValue
    }}</a>
    <a v-if="valueType === 'IMAGE'" :href="normalizeUrlValue(dataValue)" target="_blank" rel="noopener">
      <img :src="normalizeUrlValue(dataValue)" :alt="`Afbeelding ${dataKey}`" :style="{ maxWidth: '100%' }" />
    </a>
    <span v-if="valueType === 'ARRAY' || valueType === 'OBJECT'">
      <Button
        class="tw-flex-shrink-0"
        size="small"
        text
        icon="pi pi-external-link"
        label="Bekijken"
        @click="visible = true"
    /></span>
  </div>

  <Drawer v-model:visible="visible" modal :header="dialogTitle" :position="position" class="!tw-w-full md:!tw-w-1/2">
    <div class="tw-mb-4">
      <DataTable
        v-if="isComplexArray(dataValue) || valueType === 'OBJECT'"
        :value="valueType === 'OBJECT' ? [dataValue] : dataValue"
        size="small"
        scrollable
        scroll-height="260px"
        responsive-layout="scroll"
        class="tw-w-full"
      >
        <Column v-for="col in objectTableColumns" :key="col" :field="col" :header="prettyHeader(col)">
          <template #body="{ data }">
            <!-- render nested values compactly -->
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
            <RichValue :data-key="i" :data-value="item" :position="position" />
          </li>
        </ul>
      </div>

      <div v-else class="tw-mb-4">Kan de waarde niet weergeven. Ongeldig formaat.</div>
    </div>
  </Drawer>
</template>

<script>
import Markdown from "./Markdown";
import { normalizeUrlValue } from "@/utils/rich-value";
import { formatRawString } from "@/utils/string-helpers";

const imageRegex = /^(http|https).*(\.jpg|\.jpeg|\.png|\.gif)/;
const urlRegex = /^(http|https)/;
const dateRegex = /^(\d{4})-(\d{2})-(\d{2})Z/;

export default {
  name: "RichValue",
  components: {
    Markdown,
  },
  props: {
    dataKey: String,
    dataValue: [String, Number, Object, Array, Boolean, null],
    position: {
      type: String,
      default: "right",
    },
  },
  data() {
    return {
      visible: false,
    };
  },
  computed: {
    valueType() {
      if (this.dataValue === null) {
        return "NULL";
      }

      if (Array.isArray(this.dataValue)) {
        return "ARRAY";
      }

      if (typeof this.dataValue === "object" && !Array.isArray(this.dataValue)) {
        return "OBJECT";
      }

      if (typeof this.dataValue === "number") {
        return "NUMBER";
      }

      if (typeof this.dataValue !== "string") {
        return "UNKNOWN";
      }

      if (this.dataValue.match(imageRegex)) {
        return "IMAGE";
      }

      if (this.dataValue.match(urlRegex)) {
        return "URL";
      }

      if (this.dataValue.match(dateRegex)) {
        return "DATE";
      }

      return "STRING";
    },
    objectTableColumns() {
      if (this.valueType === "OBJECT") {
        return Object.keys(this.dataValue);
      }

      if (!Array.isArray(this.dataValue)) return [];
      const sample = this.dataValue.slice(0, 50).filter((x) => x && typeof x === "object" && !Array.isArray(x));

      const keys = new Set();
      for (const row of sample) Object.keys(row).forEach((k) => keys.add(k));

      return Array.from(keys);
    },
    dialogTitle() {
      return this.dataKey ? this.prettyHeader(this.dataKey) : "Waarde";
    },
  },
  methods: {
    normalizeUrlValue,
    friendlyDate(value) {
      const parsedDate = dateRegex.exec(value);
      return `${parsedDate[3]}-${parsedDate[2]}-${parsedDate[1]}`;
    },
    prettyHeader(key) {
      return formatRawString(key);
    },
    isSimpleArray(arr) {
      return Array.isArray(arr) && arr.length > 0 && (typeof arr[0] !== "object" || arr[0] === null);
    },
    isComplexArray(arr) {
      return (
        Array.isArray(arr) && arr.length > 0 && typeof arr[0] === "object" && arr[0] !== null && !Array.isArray(arr[0])
      );
    },
  },
};
</script>
