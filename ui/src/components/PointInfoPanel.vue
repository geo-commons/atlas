<template>
  <div>
    <button v-if="!showSidePanel && showInfoPanel" @click="toggleSidePanel" v-tippy='{ placement : "right" }' content="Toon details" aria-label="Toon details" class="iconbutton open-button">
      <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none"/><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
    </button>

    <SidePanel :showPanel="showInfoPanel && showSidePanel" @toggle-side-panel="toggleSidePanel">
      <template v-slot:search>
        <button class="iconbutton back-button" type="button" v-tippy='{ placement : "right" }' content="Ga terug" aria-label="Ga terug" @click="closeInfoPanel">
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M19 11H7.83l4.88-4.88c.39-.39.39-1.03 0-1.42-.39-.39-1.02-.39-1.41 0l-6.59 6.59c-.39.39-.39 1.02 0 1.41l6.59 6.59c.39.39 1.02.39 1.41 0 .39-.39.39-1.02 0-1.41L7.83 13H19c.55 0 1-.45 1-1s-.45-1-1-1z"/></svg>
        </button>
        <h1>{{searchQuery}}</h1>
      </template>

      <template v-slot:default>
        <FeatureInfo v-for="visibleLayer in visibleLayers" :isOpen="visibleLayers.length === 1" v-bind:key="visibleLayer.id" :layer="visibleLayer" :position="position" />
      </template>
    </SidePanel>
  </div>
</template>

<script>
import SidePanel from './SidePanel'
import FeatureInfo from './FeatureInfo'

export default {
  name: 'MorePanel',
  components: {
    SidePanel,
    FeatureInfo,
  },
  methods: {
    closeInfoPanel() {
      this.searchQuery = ''
      this.$emit('set-position', { ...this.position, marker: null })
    },
    toggleSidePanel() {
      this.$emit('toggle-side-panel')
    }
  },
  computed: {
    visibleLayers() {
      return this.layers.filter((layer) => layer.is_visible && !layer.is_base)
    },
    searchQuery: {
      get() {
        return this.$store.state.searchQuery
      },
      set(value) {
        this.$store.commit('setSearchQuery', value)
      }
    }
  },
  props: {
    position: Object,
    layers: Array,
    showSidePanel: Boolean,
    showInfoPanel: Boolean
  },
}
</script>

<style scoped>
.open-button {
  position: fixed;
  top: var(--padding-screen);
  z-index: 1;
  width: 24px;
  height: var(--width-button-large);
  background: white;
  border-top-right-radius: var(--radius-small);
  border-bottom-right-radius: var(--radius-small);
  box-shadow: var(--shadow-normal);
}

h1 {
  font-size: var(--font-size-normal);
}

.back-button {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-normal);
  border: 1px solid var(--color-grey-60);
}
</style>
