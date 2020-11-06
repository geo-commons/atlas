<template>
  <div class="container">
    <div class="interface">
      <SearchPanel />
      <LayersPanel :layers="this.layers" />
      <ZoomPanel :position="this.position" @set-position="this.setPosition" />
      <MorePanel />
    </div>
    <Map :position="this.position" :layers="this.layers" @set-position="this.setPosition" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Map from '../components/Map'
import SearchPanel from '../components/SearchPanel'
import LayersPanel from '../components/LayersPanel'
import ZoomPanel from '../components/ZoomPanel'
import MorePanel from '../components/MorePanel'

export default {
  name: 'App',
  components: {
    Map,
    SearchPanel,
    LayersPanel,
    ZoomPanel,
    MorePanel,
  },
  computed: mapState({
    position: state => state.position,
    layers: state => state.layers,
  }),
  methods: {
    setPosition(position) {
      this.$store.commit('setPosition', position)
    },
  }
}
</script>

<style scoped>
.container {
  width: 100%;
  height: 100%;
}
.interface {
  position: absolute;
  z-index: 1;
}
</style>
