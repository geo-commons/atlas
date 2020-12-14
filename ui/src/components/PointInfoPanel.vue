<template>
  <div>
    <button v-if="this.position.marker && !showInfoPanel" @click="toggleSidePanel" aria-label="Toon details" class="iconbutton open-button">
      <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none"/><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
    </button>

    <transition name="fade">
      <aside class="wrapper" v-if="showInfoPanel">
        <button @click="toggleSidePanel" aria-label="Verberg details" class="iconbutton close-button">
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M15.41 7.41L14 6l-6 6 6 6 1.41-1.41L10.83 12l4.58-4.59z"/></svg>
        </button>

        <div class="content">
          <FeatureInfo v-for="visibleLayer in visibleLayers" v-bind:key="visibleLayer.id" :layer="visibleLayer" :position="position" />
        </div>
      </aside>
    </transition>
  </div>
</template>

<script>
import FeatureInfo from './FeatureInfo'

export default {
  name: 'MorePanel',
  components: {
    FeatureInfo
  },
  methods: {
    toggleSidePanel() {
      this.$emit('toggle-side-panel')
    }
  },
  computed: {
    visibleLayers() {
      return this.layers.filter((layer) => layer.is_visible && !layer.is_base)
    }
  },
  props: {
    position: Object,
    layers: Array,
    showInfoPanel: Boolean
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
  background: white;
  box-shadow: var(--shadow-normal);
}

.content {
  width: 100vw;
  max-width: var(--width-detail);
  max-height: calc(100% - (var(--padding-screen) + var(--width-button-large)));
  overflow-y: auto;
  margin-top: calc(var(--padding-screen) + var(--width-button-large));
  padding: 20px;
}

.close-button,
.open-button {
  width: 24px;
  height: var(--width-button-large);
  background: white;
  border-top-right-radius: var(--radius-small);
  border-bottom-right-radius: var(--radius-small);
  box-shadow: var(--shadow-normal);
}

.close-button {
  position: absolute;
  top: var(--padding-screen);
  right: -24px;
}

.close-button:before {
  content: '';
  position: absolute;
  top: 0;
  bottom: 0;
  width: 20px;
  left: -20px;
  background: white;
  pointer-events: none;
}

.open-button {
  position: fixed;
  top: var(--padding-screen);
  z-index: 1;
}
</style>
