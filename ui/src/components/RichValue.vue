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

  <Drawer
    v-if="config.style.complex_data_display === 'panel'"
    v-model:visible="visible"
    modal
    :header="dialogTitle"
    :position="position"
    class="!tw-w-full md:!tw-w-1/2"
  >
    <ComplexData :data-value="dataValue" :value-type="valueType" :position="position" />
  </Drawer>
  <Dialog v-else v-model:visible="visible" modal :header="dialogTitle" class="tw-w-full md:tw-w-1/2">
    <ComplexData :data-value="dataValue" :value-type="valueType" :position="position" />
  </Dialog>
</template>

<script>
import Markdown from "./Markdown";
import { normalizeUrlValue } from "@/utils/rich-value";
import { formatRawString } from "@/utils/string-helpers";
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";

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
    ...mapState(useGlobalStore, ["config"]),
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
  },
};
</script>
