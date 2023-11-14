<template>
  <span class="status-wrapper">
    <CircleCheckIcon v-if="status" class="icon __green" />
    <CircleCrossIcon v-else class="icon __red"
  /></span>
</template>

<script>
import CircleCrossIcon from "@/assets/icons/circle-cross-icon.svg";
import CircleCheckIcon from "@/assets/icons/circle-check-icon.svg";

export default {
  name: "StatusIndicatorComponent",
  components: { CircleCheckIcon, CircleCrossIcon },
  props: {
    status: Boolean,
  },
};
</script>

<style scoped>
.status-wrapper {
  display: flex;
  align-items: center;
}
</style>
