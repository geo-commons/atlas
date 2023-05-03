<template>
  <Markdown :source="parsedSource" />
</template>

<script>
import nunjucks from "nunjucks";
import Markdown from "./Markdown";

nunjucks.configure({ autoescaping: true });

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
        return nunjucks.renderString(this.source, this.data);
      } catch (e) {
        return "";
      }
    },
  },
};
</script>
