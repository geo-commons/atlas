<template>
  <div>
    <h3>Kaartlaag instellingen bewerken</h3>

    <div class="">
      <input id="is_visible" v-model="layer.settings.is_visible" type="checkbox" name="is_visible" />
      <label for="is_visible">Toon laag</label>
    </div>
  </div>
</template>

<script>
export default {
  name: "MapLayer",
  props: {
    initialLayerData: Object,
  },
  data() {
    return {
      layer: null,
    };
  },
  created() {
    this.layer = this.initialLayerData;
  },
};
</script>

<style scoped></style>
