<template>
  <div>
    <span v-if="valueType === 'NUMBER'">{{ dataValue }}</span>
    <span v-if="valueType === 'UNKNOWN'">{{ dataValue }}</span>
    <span v-if="valueType === 'DATE'">{{ friendlyDate(dataValue) }}</span>
    <markdown v-if="valueType === 'STRING'" :source="dataValue" />
    <a
      v-if="valueType === 'URL'"
      :href="dataValue"
      target="_blank"
      rel="noopener"
      >{{
        dataValue.length >= 75
          ? `${dataValue.substring(0, 36)}...${dataValue.substring(
              dataValue.length - 36
            )}`
          : dataValue
      }}</a
    >
    <a
      v-if="valueType === 'IMAGE'"
      :href="dataValue"
      target="_blank"
      rel="noopener"
    >
      <img
        :src="dataValue"
        :alt="`Afbeelding ${dataKey}`"
        :style="{ maxWidth: '100%' }"
      />
    </a>
  </div>
</template>

<script>
import Markdown from "./Markdown";

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
    dataValue: [String, Number],
  },
  computed: {
    valueType() {
      if (this.dataValue === null) {
        return "NULL";
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
  },
  methods: {
    friendlyDate(value) {
      const parsedDate = dateRegex.exec(value);
      return `${parsedDate[3]}-${parsedDate[2]}-${parsedDate[1]}`;
    },
  },
};
</script>
