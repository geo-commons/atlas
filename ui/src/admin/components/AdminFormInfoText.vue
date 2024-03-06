<template>
  <tippy placement="right-end" theme="popover" trigger="click" :distance="8" :delay="[0, 0]" :a11y="null">
    <button class="iconbutton __transparent-bg" aria-label="Toon meer informatie" type="button">
      <InformationCircleIcon />
    </button>
    <template #content>
      <div class="info-text">{{ infoText }}</div>
    </template>
  </tippy>
</template>

<script>
import InformationCircleIcon from "@/assets/icons/information-circle-icon.svg";
import { Tippy } from "vue-tippy";

export default {
  name: "AdminFormInfoText",
  components: { Tippy, InformationCircleIcon },
  props: {
    infoText: String,
  },
};
</script>

<style scoped>
.info-text {
  padding: 8px 16px;
  font-size: var(--font-size-normal);
}
</style>
