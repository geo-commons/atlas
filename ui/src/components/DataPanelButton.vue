<template>
  <button
    v-tippy="{ placement: 'bottom' }"
    class="iconbutton toggle-button"
    type="button"
    content="Toon data"
    aria-label="Toon data"
    @click="showDataPanel"
  >
    <FormIcon />
  </button>
</template>

<script>
import FormIcon from "../icons/FormIcon.vue";

export default {
  name: "DataPanelButton",
  components: {
    FormIcon,
  },
  methods: {
    showDataPanel() {
      this.$emit("show-data-panel");
    },
  },
};
</script>

<style scoped>
.toggle-button {
  width: var(--width-button-large);
  border-right: 1px solid var(--color-grey-50);
}

.iconbutton:not([disabled]):hover:before {
  background: var(--color-grey-40);
}

.iconbutton:not([disabled]):active:before {
  background: var(--color-grey-50);
}
</style>
