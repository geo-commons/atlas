<template>
  <SidePanel large :showPanel="showDataPanel">
    <template v-slot:search>
      <Search :showBorder="true" @on-close="toggleDataPanel" @on-submit="onSearch">
        <template v-slot:default>
          <input ref="queryInput" type="search" name="search" placeholder="Zoek data" autocomplete="off" />
        </template>
      </Search>
    </template>

    <template v-slot:default>
      <FeatureTable
        v-for="visibleLayer in visibleLayers"
        v-bind:key="visibleLayer.id"
        :isOpen="visibleLayers.length === 1"
        :layer="visibleLayer"
        :position="position"
        :selectedArea="selectedArea"
        :query="query"
      />
    </template>
  </SidePanel>
</template>

<script>
import SidePanel from './SidePanel'
import FeatureTable from './FeatureTable'
import Search from './Search'

export default {
  name: 'DataPanel',
  components: {
    SidePanel,
    FeatureTable,
    Search
  },
  methods: {
    onSearch() {
      this.query = this.$refs.queryInput.value
    },
    toggleDataPanel() {
      this.$emit('toggle-data-panel')
    },
  },
  computed: {
    visibleLayers() {
      return this.layers.filter((layer) => layer.is_visible && !layer.is_base)
    }
  },
  data() {
    return {
      query: ''
    }
  },
  props: {
    position: Object,
    layers: Array,
    showDataPanel: Boolean,
    selectedArea: Object
  }
}
</script>