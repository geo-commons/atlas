<template>
  <div>
    <button v-if="!showSidePanel && showInfoPanel" @click="toggleSidePanel" v-tippy='{ placement : "right" }' content="Toon details" aria-label="Toon details" class="iconbutton open-button">
      <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none"/><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
    </button>

    <SidePanel :showPanel="showInfoPanel && showSidePanel" @toggle-side-panel="toggleSidePanel">
      <template v-slot:search>
        <Search :show-border="true" @on-close="closeInfoPanel">
          <template v-slot:default>
            <input type="text" name="search" placeholder="Zoek adres" autocomplete="off" />
          </template>
        </Search>
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
import Search from './Search'

export default {
  name: 'MorePanel',
  components: {
    SidePanel,
    FeatureInfo,
    Search
  },
  methods: {
    closeInfoPanel() {
      this.$emit('set-position', { ...this.position, marker: null })
    },
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
</style>
