<template>
  <div class="panel" :class="{ expand }">
    <div class="panel-header" @click="toggleExpand">
      <slot name="header">
        <ChevronUpIcon v-if="!expand" class="expand-icon" />
        <ChevronDownIcon v-else class="expand-icon" />

        <h3>{{ title }}</h3>
        <PrimaryButton class="close-btn" size="large" @click="hidePanel">
          <close-icon />
        </PrimaryButton>
      </slot>
    </div>
    <div ref="content" class="content">
      <slot v-if="!loading"></slot>
      <Spinner v-else :size="'medium'" />
    </div>
  </div>
</template>

<script>
import PrimaryButton from "./PrimaryButton.vue";
import Spinner from "@/components/Spinner.vue";
import CloseIcon from "../assets/icons/close-icon.svg";
import ChevronUpIcon from "../assets/icons/chevron-up-icon.svg";
import ChevronDownIcon from "../assets/icons/chevron-down-icon.svg";

export default {
  name: "PanelDisplay",
  components: {
    ChevronUpIcon,
    ChevronDownIcon,
    CloseIcon,
    PrimaryButton,
    Spinner,
  },
  props: {
    id: Number,
    title: String,
    goBack: Function,
    loading: Boolean,
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
  z-index: 2;
  background: white;
  box-shadow: var(--shadow-normal);
  display: flex;
  flex-direction: column;
}

.panel-header {
  display: flex;
  gap: 8px;
  align-items: center;
  border-bottom: 1px solid var(--color-grey-30);
}

@media (max-width: 575px) {
  .panel {
    height: calc(40 * var(--vh));
  }

  .panel.expand {
    height: 100%;
  }

  .panel-header {
    padding: 8px 16px;
    cursor: pointer;
  }
}

@media (min-width: 576px) {
  .panel {
    height: 100%;
    max-width: var(--width-detail);
  }

  .panel.expand {
    max-width: 100%;
  }

  .panel-header {
    padding: 12px 16px;
  }

  .expand-icon {
    display: none;
  }
}

.close-btn {
  margin-left: auto;
}

h3 {
  font-size: var(--font-size-large);
}

.content {
  overflow-y: auto;
}
</style>
