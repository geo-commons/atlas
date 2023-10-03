<template>
  <div class="container">
    <div class="section">
      <h1>todo: edit layer</h1>
    </div>
  </div>
</template>

<script>
// import { ValidationObserver, ValidationProvider } from "vee-validate";

export default {
  name: "LayerCreateUpdate",
  components: {
    // ValidationObserver,
    // ValidationProvider,
  },
  data() {
    return {
      data: null,
      layersFromCapabilities: [],
    };
  },
  created() {},
  methods: {},
};
</script>

<style scoped>
.flexer {
  display: flex;
  margin-top: 20px;
  justify-content: left;
}

.section {
  max-width: 600px;
}
</style>
