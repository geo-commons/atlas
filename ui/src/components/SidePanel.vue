<template>
  <aside v-if="showPanel" class="wrapper" :class="{ large, medium, fullScreen }">
    <button
      v-if="(large || medium) && !fullScreen"
      v-tippy="{ placement: 'right' }"
      :content="large && medium ? 'Verklein paneel' : 'Vergroot paneel'"
      :aria-label="large && medium ? 'Verklein paneel' : 'Vergroot paneel'"
      class="iconbutton resize-button"
      @click="toggleSidePanel"
    >
      <ChevronLeftIcon v-if="large && medium" />
      <ChevronRightIcon v-else />
    </button>
    <button
      v-tippy="{ placement: 'bottom' }"
      :content="fullScreen ? 'Verklein paneel' : 'Vergroot paneel'"
      :aria-label="fullScreen ? 'Verklein paneel' : 'Vergroot paneel'"
      class="iconbutton expand-mobile-button"
      @click="toggleFullScreen"
    >
      <ChevronUpIcon />
    </button>
    <button
      v-if="large && fullScreen"
      v-tippy="{ placement: 'left' }"
      content="Verklein paneel"
      aria-label="Verklein paneel"
      class="iconbutton resize-button exit-fullscreen"
      @click="toggleSidePanel"
    >
      <ChevronLeftIcon />
    </button>

    <div class="header">
      <slot name="search"></slot>
    </div>

    <div class="content">
      <slot></slot>
    </div>
  </aside>
</template>

<script>
import ChevronRightIcon from "@/assets/icons/chevron-right-icon.svg";
import ChevronLeftIcon from "@/assets/icons/chevron-left-icon.svg";
import ChevronUpIcon from "@/assets/icons/chevron-up-icon.svg";

export default {
  name: "SidePanel",
  components: { ChevronRightIcon, ChevronLeftIcon, ChevronUpIcon },
  props: {
    initialSizeLarge: Boolean,
    initialSizeMedium: Boolean,
    showPanel: Boolean,
  },
  data() {
    return {
      fullScreen: false,
      large: false,
      medium: false,
    };
  },
  created() {
    this.large = this.initialSizeLarge;
    this.medium = this.initialSizeMedium;
  },
  watch: {
    initialSizeLarge(value) {
      this.large = value;
      this.fullScreen = false;
    },
  },
  methods: {
    toggleSidePanel() {
      if (!this.medium) {
        this.toggleFullScreen();
        return;
      }

      this.large = !this.large;
      this.$emit("expand-side-panel", this.large);
    },
    toggleFullScreen() {
      this.fullScreen = !this.fullScreen;
      this.$emit("toggle-full-side-panel");
    },
  },
};
</script>

<style scoped>
.wrapper {
  position: relative;
  flex-shrink: 0;
  z-index: 2;
  width: 100%;
  background: white;
  box-shadow: var(--shadow-normal);
  display: flex;
  flex-direction: column;
}

@media (min-width: 1024px) {
  .wrapper {
    height: 100%;
    max-width: var(--width-detail);
  }

  .wrapper.large {
    max-width: 50%;
  }

  .wrapper.fullScreen {
    max-width: 100%;
  }
}

@media (max-width: 932px) {
  .wrapper {
    height: calc(40 * var(--vh));
    width: 100%;
  }

  .wrapper.fullScreen {
    height: 100%;
  }
}

.header {
  display: flex;
  width: 100%;
  padding: var(--padding-screen);
  padding-bottom: 0;
}

.content {
  position: relative;
  flex-grow: 1;
  overflow-y: auto;
  padding: 16px 0;
}

.resize-button {
  position: absolute;
  top: var(--padding-screen);
  right: -24px;
  width: 24px;
  height: var(--width-button-large);
  border-top-right-radius: var(--radius-small);
  border-bottom-right-radius: var(--radius-small);
  background: white;
  box-shadow: var(--shadow-normal);
}

.resize-button:before {
  content: "";
  position: absolute;
  top: -8px;
  bottom: -8px;
  width: 8px;
  left: -8px;
  background: white;
  pointer-events: none;
}

@media (max-width: 932px) {
  .resize-button {
    display: none;
  }

  .fullScreen .header {
    padding-top: 36px;
  }
}

.expand-mobile-button {
  position: absolute;
  background: white;
  box-shadow: var(--shadow-normal);
  width: var(--width-button-large);
  height: 24px;
  top: -24px;
  left: 0;
  right: 0;
  margin: 0 auto;
  border-top-left-radius: var(--radius-small);
  border-top-right-radius: var(--radius-small);
  z-index: 1;
}

.wrapper.fullScreen .expand-mobile-button {
  top: 0;
  border: 1px solid var(--color-grey-60);
  border-top: none;
  box-shadow: none;
  border-radius: 0;
  border-bottom-left-radius: var(--radius-small);
  border-bottom-right-radius: var(--radius-small);
}

.wrapper.fullScreen .expand-mobile-button svg {
  transform: rotate(180deg);
}

.wrapper.fullScreen .expand-mobile-button:before {
  content: none;
}

@media (min-width: 1024px) {
  .expand-mobile-button {
    display: none;
  }
}

.expand-mobile-button:before {
  content: "";
  position: absolute;
  left: -8px;
  right: -8px;
  height: 8px;
  bottom: -8px;
  background: white;
  pointer-events: none;
}

.exit-fullscreen {
  right: 1px;
  border-radius: var(--radius-small) 0 0 var(--radius-small);
  border: 1px solid var(--color-grey-60);
  border-right: none;
  box-shadow: none;
}

.exit-fullscreen:before {
  content: none;
}
</style>
