<template>
  <label class="checkbox">
    <input
      type="checkbox"
      :name="name"
      :value="value"
      :checked="checked"
      @change="$emit('change', $event)"
    />
    {{ value }}
  </label>
</template>

<script>
export default {
  name: "CheckboxField",
  props: {
    name: String,
    value: String,
    checked: Boolean,
  },
};
</script>

<style scoped>
.checkbox {
  display: flex;
  padding: 3px 0;
  cursor: pointer;
}

.checkbox > input {
  pointer-events: none;
  margin: 3px 8px 0 9px;
}
</style>
