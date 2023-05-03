<template>
  <div class="panel" :class="{ expand }">
    <div class="panel-header" @click="toggleExpand">
      <slot name="header">
        <svg
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 0 24 24"
          width="24px"
          fill="#000000"
          class="expand-icon"
        >
          <path d="M0 0h24v24H0z" fill="none" />
          <path d="M12 8l-6 6 1.41 1.41L12 10.83l4.59 4.58L18 14z" />
        </svg>
        <h3>{{ title }}</h3>
        <PrimaryButton size="large" @click="hidePanel">
          <svg
            xmlns="http://www.w3.org/2000/svg"
            height="24px"
            viewBox="0 0 24 24"
            width="24px"
            fill="#000000"
          >
            <path d="M0 0h24v24H0z" fill="none" />
            <path
              d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
            />
          </svg>
        </PrimaryButton>
      </slot>
    </div>
    <div ref="content" class="content">
      <slot></slot>
    </div>
  </div>
</template>

<script>
import PrimaryButton from "./PrimaryButton.vue";

export default {
  name: "PanelDisplay",
  components: {
    PrimaryButton,
  },
  props: {
    id: Number,
    title: String,
    goBack: Function,
  },
  data() {
    return {
      expand: false,
    };
  },
  watch: {
    id(newValue, oldValue) {
      if (newValue != oldValue) {
        this.scrollToTop();
      }
    },
  },
  methods: {
    toggleExpand() {
      this.expand = !this.expand;
    },
    hidePanel() {
      this.$emit("hidePanel");
    },
    scrollToTop() {
      this.$refs["content"].scrollTo(0, 0);
    },
  },
};
</script>

<style scoped>
.panel {
  z-index: 1;
  background: white;
  box-shadow: var(--shadow-normal);
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  align-items: center;
  border-bottom: 1px solid var(--color-grey-30);
}

.expand-icon {
  margin-right: 8px;
}

@media (max-width: 575px) {
  .panel-header {
    padding: 8px 16px;
    cursor: pointer;
  }
}

@media (min-width: 576px) {
  .panel-header {
    padding: 12px 16px;
  }

  .expand-icon {
    display: none;
  }
}

h3 {
  font-size: var(--font-size-large);
  margin: 0 auto 0 0;
}

.content {
  overflow-y: auto;
}
</style>

<style></style>
