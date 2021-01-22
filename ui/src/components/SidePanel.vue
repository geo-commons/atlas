<template>
  <div>
    <transition name="fade">
      <aside class="wrapper" :class="{ large, fullScreen }" v-if="showPanel">
        <button v-if="this.$listeners['toggle-side-panel']" @click="toggleSidePanel" v-tippy='{ placement : "right" }' content="Verberg details" aria-label="Verberg details" class="iconbutton resize-button">
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12l4.58-4.59z"/></svg>
        </button>
        <button v-if="large && !fullScreen" @click="toggleFullScreen" aria-label="Vergroot details" class="iconbutton resize-button">
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none"/><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
        </button>
        <button v-if="large && fullScreen" @click="toggleFullScreen" aria-label="Vergroot details" class="iconbutton resize-button exit-fullscreen">
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12l4.58-4.59z"/></svg>
        </button>

        <div class="header">
            <slot name="search"></slot>
        </div>

        <div class="content">
          <slot></slot>
        </div>
      </aside>
    </transition>
  </div>
</template>

<script>

export default {
  name: 'SidePanel',
  methods: {
    toggleSidePanel() {
      this.$emit('toggle-side-panel')
    },
    toggleFullScreen() {
      this.fullScreen = !this.fullScreen
    }
  },
  data() {
    return {
      fullScreen: false,
    }
  },
  props: {
    large: Boolean,
    showPanel: Boolean
  }
}
</script>

<style scoped>
.wrapper {
  position: fixed;
  z-index: 1;
  left: 0;
  top: 0;
  height: 100%;
  width: 100%;
  background: white;
  box-shadow: var(--shadow-normal);
  display: flex;
  flex-direction: column;
}

@media (min-width: 576px) {
  .wrapper {
    max-width: var(--width-detail);
  }

  .wrapper.large {
    max-width: 50%;
  }
}

.wrapper.fullScreen {
  max-width: 100%;
}

.header {
  width: 100%;
  padding: var(--padding-screen);
  padding-bottom: 0;
  margin: 0 auto;
}

.wrapper.fullScreen .header {
  max-width: var(--width-detail);
}

.content {
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
  background: white;
  border-top-right-radius: var(--radius-small);
  border-bottom-right-radius: var(--radius-small);
  box-shadow: var(--shadow-normal);
}

@media (max-width: 575px) {
  .resize-button {
    display: none;
  }
}

.resize-button:before {
  content: '';
  position: absolute;
  top: -10px;
  bottom: -10px;
  width: 10px;
  left: -10px;
  background: white;
  pointer-events: none;
}

.exit-fullscreen {
  right: 0;
  border-top-right-radius: 0;
  border-bottom-right-radius: 0;
  border-top-left-radius: var(--radius-small);
  border-bottom-left-radius: var(--radius-small);
  box-shadow: none;
  box-shadow: 0 0 0 1px var(--color-grey-60);
}

.exit-fullscreen:before {
  content: none;
}
</style>
