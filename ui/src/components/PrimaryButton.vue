<template>
  <button
    type="button"
    class="button"
    :data-size="size"
    :class="{ dropShadow, hasLabel: !!label }"
    @click="() => $emit('click')"
  >
    <slot></slot>
    <span v-if="label" class="label">{{ label }}</span>
  </button>
</template>

<script>
export default {
  name: "PrimaryButton",
  props: {
    size: {
      type: String,
      default: "normal",
    },
    dropShadow: Boolean,
    label: String,
  },
};
</script>

<style scoped>
.button {
  position: relative;
  flex-shrink: 0;
  background: white;
  color: black;
  border: 1px solid var(--color-grey-40);
  border-radius: var(--radius-normal);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: var(--font-size-small);
  font-weight: var(--font-weight-bold);
  line-height: 1;
  overflow: hidden;
}

/* Needed to lay transparent :hover/:active background on top of original background */
.button:before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
}

.button[data-size="normal"] {
  width: 32px;
  height: 32px;
}

.button[data-size="large"] {
  width: 40px;
  height: 40px;
}

.button.hasLabel {
  width: auto;
  padding: 0 12px 0 8px;
}

.label {
  margin-left: 6px;
}

.button.dropShadow {
  border: none;
  box-shadow: var(--shadow-normal);
}

.button[disabled] {
  color: var(--color-grey-60);
}

.button:not([disabled]) {
  cursor: pointer;
}

.button:not([disabled]):hover:before {
  background: var(--color-hover);
}

.button:not([disabled]):active:before {
  background: var(--color-active);
}
</style>
