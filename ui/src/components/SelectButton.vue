<template>
  <div>
    <div class="select-button-wrapper">
      <button class="select-button" :aria-controls="id" @click="onSelectItem">
        <div class="name">{{ title }}</div>
        <ChevronRightIcon />
      </button>
    </div>
  </div>
</template>

<script>
import ChevronRightIcon from "../icons/ChevronRightIcon.vue";

export default {
  name: "SelectButton",
  components: { ChevronRightIcon },
  props: {
    id: String,
    title: String,
  },
  methods: {
    onSelectItem() {
      this.$emit("select-item", this.id);
    },
  },
};
</script>

<style scoped>
.select-button-wrapper {
  display: flex;
}
.select-button {
  display: flex;
  width: 100%;
  align-items: center;
  gap: 14px;
  padding-left: var(--padding-screen);
}

.select-button:not([disabled]):hover {
  background: var(--color-grey-40);
}

.select-button:not([disabled]):active {
  background: var(--color-grey-50);
}

.name {
  padding: 6px 0;
}
</style>
