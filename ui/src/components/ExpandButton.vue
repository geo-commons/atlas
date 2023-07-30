<template>
  <div>
    <div class="expand-wrapper">
      <button
        class="expand-button"
        :aria-expanded="showContent.toString()"
        :aria-controls="id"
        @click="toggle"
      >
        <svg
          v-if="!showContent"
          xmlns="http://www.w3.org/2000/svg"
          height="24"
          viewBox="0 0 24 24"
          width="24"
        >
          <path d="M0 0h24v24H0z" fill="none" />
          <path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z" />
        </svg>
        <svg
          v-if="showContent"
          xmlns="http://www.w3.org/2000/svg"
          height="24"
          viewBox="0 0 24 24"
          width="24"
        >
          <path d="M0 0h24v24H0z" fill="none" />
          <path d="M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z" />
        </svg>
        <div class="name">{{ title }}</div>
        <slot name="button"></slot>
      </button>
      <slot name="header"></slot>
    </div>

    <div v-if="showContent" :id="id">
      <slot></slot>
    </div>
  </div>
</template>

<script>
export default {
  name: "ExpandButton",
  props: {
    id: String,
    title: String,
    isOpen: Boolean,
  },
  data() {
    return {
      showContent: this.isOpen,
    };
  },
  watch: {
    isOpen(newValue, oldValue) {
      if (newValue !== oldValue) {
        this.showContent = newValue;
      }
    },
  },
  methods: {
    toggle(e) {
      e.stopPropagation();
      this.showContent = !this.showContent;
    },
  },
};
</script>

<style scoped>
.expand-wrapper {
  display: flex;
  position: relative;
}

.expand-button {
  display: flex;
  width: 100%;
  padding-left: 4px;
}

.expand-button:not([disabled]):hover {
  background: var(--color-grey-40);
}

.expand-button:not([disabled]):active {
  background: var(--color-grey-50);
}

.expand-button > svg {
  margin-top: 4px;
  margin-right: 2px;
}

.name {
  flex-grow: 1;
  padding: 6px 0;
}
</style>
