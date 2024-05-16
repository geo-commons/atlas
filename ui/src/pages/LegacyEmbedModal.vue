<template>
  <div>
    <EmbedCode :position="position" :layers="layers" />
  </div>
</template>

<script>
import EmbedCode from "../components/EmbedCode";
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";

export default {
  name: "LegacyEmbedModal",
  components: {
    EmbedCode,
  },
  computed: mapState(useGlobalStore, ["layers", "position"]),
};
</script>
