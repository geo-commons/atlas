<template>
  <div class="feature-details-wrapper">
    <div>
      <h1>header text feature details</h1>
    </div>

    <div>
      <p>dummy content in de body</p>
    </div>
  </div>
</template>

<script>
export default {
  name: "FeatureInfoDetails",
  props: {
    feature: Object,
    layer: Object,
  },
  data() {
    return {};
  },
  computed: {},
  created() {},
  methods: {},
};
</script>

<style scoped>
.feature-details-wrapper {
  position: relative;
  flex-shrink: 0;
  z-index: 2;
  margin: var(--padding-screen);
  padding: 10px 10px;
  height: 90%;
  background: var(--color-white);
  box-shadow: var(--shadow-normal);
  border-radius: var(--radius-normal);
}
</style>
