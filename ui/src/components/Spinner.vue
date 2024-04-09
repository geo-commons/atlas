<template>
  <div class="spinner-wrapper">
    <Spinner :size="size" :line-fg-color="color" />
  </div>
</template>

<script>
import Spinner from "vue-simple-spinner";

export default {
  name: "SpinnerComponent",
  components: {
    Spinner,
  },
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
    this.color =
      this.styleType === "admin"
        ? window.getComputedStyle(document.documentElement).getPropertyValue("--color-admin-primary")
        : window.getComputedStyle(document.documentElement).getPropertyValue("--color-primary");
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
