<template>
  <MapRenderer
    ref="map"
    class="editor-map"
    :features="features"
    :initial-layers="layers"
    :initial-position="position"
    :settings="settings"
    :user="user"
    :admin-map="true"
    @update-user-settings="updateUserSettings"
  />
</template>

<script>
import MapRenderer from "@/components/MapRenderer/MapRenderer";

export default {
  name: "MapPreview",
  components: { MapRenderer },
  props: {
    features: {
      type: Object,
      required: true,
    },
    layers: {
      type: Array,
      required: true,
    },
    position: {
      type: Object,
      required: false,
    },
    settings: {
      type: Object,
      required: true,
    },
    user: {
      type: Object,
      required: false,
      default: null,
    },
  },
  methods: {
    updateUserSettings(value) {
      this.$emit("update-user-settings", value);
    },
  },
};
</script>

<style>
.editor-map {
  width: 100%;
  height: 100vh;
  z-index: 0;
  overflow: hidden;
}
</style>
