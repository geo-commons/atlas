<template>
  <Transition name="slide">
    <aside
      v-if="showPanel"
      class="wrapper"
      :class="{ large, medium, fullScreen }"
      :style="{ width: fullScreen ? '100%' : large && !resizable ? '50%' : panelWidth }"
      :data-testid="testId"
    >
      <div class="wrapper-content tw-max-h-full">
        <template v-if="$slots.header">
          <slot name="header"></slot>
        </template>

        <div v-if="$slots.search" class="header tw-mb-4">
          <slot name="search"></slot>
        </div>

        <div class="content">
          <slot></slot>
        </div>

        <footer v-if="$slots.footer" class="tw-w-full tw-bg-white">
          <div class="tw-px-3">
            <hr class="tw-my-0 tw-border-t tw-border-gray-200" />
          </div>
          <slot name="footer"></slot>
        </footer>
      </div>

      <div v-if="resizable" class="resizer" @mousedown="initResize"></div>

      <button
        v-if="(large || medium) && !fullScreen && expandable"
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
        :class="{ 'expand-mobile-button--expanded': fullScreen }"
        @click="toggleFullScreen"
      >
        <ChevronUpIcon />
      </button>
      <button
        v-if="large && fullScreen && expandable"
        v-tippy="{ placement: 'left' }"
        content="Verklein paneel"
        aria-label="Verklein paneel"
        class="iconbutton resize-button exit-fullscreen"
        @click="toggleSidePanel"
      >
        <ChevronLeftIcon />
      </button>
    </aside>
  </Transition>
</template>

<script>
import ChevronLeftIcon from "@/assets/icons/chevron-left-icon.svg";
import ChevronRightIcon from "@/assets/icons/chevron-right-icon.svg";
import ChevronUpIcon from "@/assets/icons/chevron-up-icon.svg";

export default {
  name: "SidePanel",
  components: { ChevronRightIcon, ChevronLeftIcon, ChevronUpIcon },
  props: {
    initialSizeLarge: Boolean,
    initialSizeMedium: Boolean,
    resizable: {
      type: Boolean,
      default: false,
    },
    showPanel: Boolean,
    expandable: {
      type: Boolean,
      default: true,
    },
    testId: {
      type: String,
      default: null,
    },
  },
  emits: ["expand-side-panel", "toggle-full-side-panel", "resize"],
  data() {
    return {
      fullScreen: false,
      large: false,
      medium: false,
      panelWidth: "400px",
      isResizing: false,
    };
  },
  created() {
    this.large = this.initialSizeLarge;
    this.medium = this.initialSizeMedium;

    if (this.initialSizeLarge && this.resizable) {
      this.panelWidth = "50%";
    }
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
    initResize(e) {
      this.isResizing = true;
      document.addEventListener("mousemove", this.resizePanel);
      document.addEventListener("mouseup", this.stopResize);

      // prevent text selection
      e.preventDefault();
    },
    resizePanel(e) {
      if (!this.isResizing) return;
      const newWidth = e.clientX;
      if (newWidth > window.innerWidth * 0.25 && newWidth < window.innerWidth * 0.9) {
        this.panelWidth = newWidth + "px";
      }
    },
    stopResize() {
      this.isResizing = false;
      document.removeEventListener("mousemove", this.resizePanel);
      document.removeEventListener("mouseup", this.stopResize);
      this.$emit("resize", this.panelWidth);
    },
    toggleFullScreen() {
      this.fullScreen = !this.fullScreen;
      if (this.fullScreen) this.panelWidth = window.innerWidth + "px";
      this.$emit("toggle-full-side-panel");
    },
  },
};
</script>

<style scoped lang="scss">
.wrapper {
  position: relative;
  flex-shrink: 0;
  z-index: 2;
  overflow: unset;
  background: white;
  box-shadow: var(--shadow-normal);
  display: flex;
  flex-direction: column;
  transition:
    max-width 0.3s ease,
    height 0.3s ease,
    width 0.3s ease;
}

.wrapper-content {
  position: relative;
  z-index: 2;
  display: flex;
  flex-direction: column;
  flex-grow: 1;
  width: var(--width-detail);
  transition: width 0.3s ease;

  @media (max-width: 932px) {
    &:has(.about-panel__content) {
      display: unset;
      height: calc(40 * var(--vh));
      overflow-y: auto;
    }
  }
}

@media (min-width: 1200px) {
  .wrapper.large {
    width: 25%;
    max-width: 50vw;
    min-width: 25vw;
  }
}

@media (min-width: 1025px) {
  .wrapper {
    height: 100%;
    max-width: var(--width-detail);
    width: var(--width-detail);
  }

  .wrapper.large {
    width: 50%;
    max-width: 50vw;

    .wrapper-content {
      width: 100%;
    }
  }

  .wrapper.fullScreen {
    max-width: 100%;
    width: 100%;
  }

  .resizer {
    width: 5px;
    cursor: ew-resize;
    position: absolute;
    top: 0;
    right: 0;
    height: 100%;
    z-index: 10;
    background: transparent;
  }
}

@media (max-width: 1024px) {
  .wrapper {
    height: calc(40 * var(--vh));
    max-width: 100%;

    .wrapper-content {
      width: 100%;
    }
  }

  .wrapper.medium {
    min-width: 100%;
  }

  .wrapper.large {
    width: 100%;
    min-width: 100%;
  }

  .wrapper.fullScreen {
    height: 100%;
  }

  .resizer {
    display: none;
  }
}

.header {
  background-color: var(--color-white);
  display: flex;
  width: 100%;
  padding: var(--padding-screen);
  padding-bottom: 0;
  z-index: 2;
}

.content {
  position: relative;
  flex-grow: 1;
  overflow-y: auto;
  overflow-wrap: break-word;
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
  z-index: 1;
}

@media (max-width: 1024px) {
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

  &--expanded {
    z-index: 3;
  }
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

@media (min-width: 1025px) {
  .expand-mobile-button {
    display: none;
  }
}

.exit-fullscreen {
  right: 1px;
  z-index: 10;
  border-radius: var(--radius-small) 0 0 var(--radius-small);
  border: 1px solid var(--color-grey-60);
  border-right: none;
  box-shadow: none;
}

.slide-enter-active,
.slide-leave-active {
  overflow: hidden;
  transition:
    opacity 0.3s ease-out,
    max-width 0.3s ease-out;

  @media (max-width: 1024px) {
    transition:
      opacity 0.3s ease-out,
      max-height 0.3s ease-out;
  }
}

.slide-enter-from,
.slide-leave-to {
  opacity: 0;
  max-width: 0;
}

@media (min-width: 1025px) {
  .slide-enter-from,
  .slide-leave-to {
    opacity: 0;
    max-width: 0;
  }
}

@media (max-width: 1024px) {
  .slide-enter-from,
  .slide-leave-to {
    opacity: 0;
    max-height: 0;
    max-width: 100%;
  }
}
</style>
