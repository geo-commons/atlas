<template>
  <Markdown :source="parsedSource" />
</template>

<script>
import { renderTemplate } from "@/utils/template-renderer";
import Markdown from "./Markdown";

export default {
  name: "MarkdownTemplate",
  components: {
    Markdown,
  },
  props: {
    source: String,
    data: Object,
  },
  computed: {
    parsedSource() {
      try {
        return renderTemplate(this.source, this.data);
      } catch {
        return "";
      }
    },
  },
};
</script>
