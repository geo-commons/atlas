<template>
  <div class="container">
    <div class="interface">
      <SearchPanel :position="this.position" @set-position="this.setPosition" />
      <LayersPanel :layers="this.layers" @toggle-layer="this.toggleLayer" />
      <ZoomPanel :position="this.position" @set-position="this.setPosition" />
      <BaseLayersPanel :layers="this.layers" @toggle-layer="this.toggleLayer" />
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
import BaseLayersPanel from '../components/BaseLayersPanel'

export default {
  name: 'App',
  components: {
    Map,
    SearchPanel,
    LayersPanel,
    ZoomPanel,
    MorePanel,
    BaseLayersPanel
  },
  computed: mapState({
    position: state => state.position,
    layers: state => state.layers,
  }),
  methods: {
    setPosition(position) {
      this.$store.commit('setPosition', position)
    },
    toggleLayer(layer) {
      this.$store.commit('toggleLayer', layer)
    }
  }
}
</script>

<style>
@import url('https://rsms.me/inter/inter.css');
html { font-family: 'Inter', sans-serif; letter-spacing: -0.035em; font-size: 15px; }
@supports (font-variation-settings: normal) {
  html { font-family: 'Inter var', sans-serif; letter-spacing: -0.035em; }
}

 *,
  *:after,
  *:before {
      box-sizing: border-box;
  }

/* Remove outline from all focused elements */
*:focus {
  outline: none;
}

/* Remove highlight color on Android */
* {
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
}

input, button {
  padding: 0;
  border: none;
  background: transparent;
  font: inherit;
  letter-spacing: inherit;
}

input::placeholder {
  color: rgba(0,0,0,.55);
}

button:not([disabled]) {
  cursor: pointer;
}

button:not([disabled]):hover {
  background: #F5F5F5;
}

button:not([disabled]):active {
  background: #EAEAEA;
}

ul {
  margin: 0;
  padding: 0;
  list-style-type: none;
}

.iconbutton {
  display: flex;
  align-items: center;
  justify-content: center;
}
</style>

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
