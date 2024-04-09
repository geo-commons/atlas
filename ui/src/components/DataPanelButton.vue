<template>
  <button
    v-tippy="{ placement: 'bottom' }"
    class="iconbutton toggle-button"
    :class="{ isActive: showDataPanel }"
    type="button"
    :content="showDataPanel ? 'Verberg data' : 'Toon data'"
    :aria-label="showDataPanel ? 'Verberg data' : 'Toon data'"
    @click="toggleDataPanel"
  >
    <FormIcon />
  </button>
</template>

<script>
import FormIcon from "../assets/icons/form-icon.svg";

export default {
  name: "DataPanelButton",
  components: {
    FormIcon,
  },
  props: {
    showDataPanel: Boolean,
  },
  methods: {
    toggleDataPanel() {
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
