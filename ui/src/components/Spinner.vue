<template>
  <div class="spinner-wrapper">
    <ProgressSpinner stroke-width="2" fill="transparent" :style="{ stroke: color }" />
  </div>
</template>

<script>
export default {
  name: "SpinnerComponent",
  props: {
    size: {
      type: String,
      default: "huge",
    },

    styleType: {
      type: String,
      default: "",
    },
  },
  data() {
    return {
      color: null,
    };
  },
  created() {
    this.color = this.getColor(this.styleType);
  },
  methods: {
    getColor(styleType) {
      switch (styleType) {
        case "admin":
          return "#424bff";
        default:
          return "#0066ff";
      }
    },
  },
};
</script>

<style scoped>
.spinner-wrapper {
  min-height: 400px;
  display: flex;
  align-items: center;
  justify-content: center;
}

@media (max-width: 576px) {
  .spinner-wrapper {
    min-height: 150px;
  }
}
</style>
