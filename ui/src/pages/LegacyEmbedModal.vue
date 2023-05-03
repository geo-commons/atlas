<template>
  <div>
    <EmbedCode :position="position" :layers="layers" />
  </div>
</template>

<script>
import { mapState } from "vuex";
import EmbedCode from "../components/EmbedCode";

export default {
  name: "LegacyEmbedModal",
  components: {
    EmbedCode,
  },
  computed: mapState({
    position: (state) => state.position,
    layers: (state) => state.layers,
  }),
};
</script>
