<template>
  <div class="container">
    <div class="interface">
      <SearchPanel :position="this.position" @set-position="this.setPosition" />
      <LayersPanel :layers="this.layers" @toggle-layer="this.toggleLayer" />
      <div class="top-right-panels">
        <MeasurePanel :measure="this.measure" @set-measure="this.setMeasure" />
        <MorePanel />
      </div>
      <div class="bottom-right-panels">
        <BaseLayersPanel :layers="this.layers" @toggle-layer="this.toggleLayer" />
        <ZoomPanel :position="this.position" @set-position="this.setPosition" />
      </div>
    </div>
    <Map :position="this.position" :layers="this.layers" :measure="this.measure" @set-position="this.setPosition" />
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Map from '../components/Map'
import SearchPanel from '../components/SearchPanel'
import LayersPanel from '../components/LayersPanel'
import ZoomPanel from '../components/ZoomPanel'
import MorePanel from '../components/MorePanel'
import MeasurePanel from '../components/MeasurePanel'
import BaseLayersPanel from '../components/BaseLayersPanel'

export default {
  name: 'App',
  components: {
    Map,
    SearchPanel,
    LayersPanel,
    ZoomPanel,
    MorePanel,
    MeasurePanel,
    BaseLayersPanel,
  },
  computed: mapState({
    position: state => state.position,
    layers: state => state.layers,
    measure: state => state.measure,
  }),
  methods: {
    setPosition(position) {
      this.$store.commit('setPosition', position)
    },
    toggleLayer(layer) {
      this.$store.commit('toggleLayer', layer)
    },
    setMeasure(measure) {
      this.$store.commit('setMeasure', measure)
    }
  }
}
</script>

<style>
  :root {
    --color-primary: #0066FF;
    --color-grey-50: #EAEAEA;

    --font-size-small: 14px;
    --font-size-normal: 16px;

    --font-weight-normal: 400;
    --font-weight-bold: 700;

    --radius-small: 3px;
    --radius-normal: 6px;

    --shadow-normal: 0 0 4px rgba(0,0,0,.1), 0 0 12px rgba(0,0,0,.15);

    --padding-screen: 8px;

    --width-detail: 350px;
    --width-button-normal: 32px;
    --width-button-large: 40px;
  }

  @import url('https://fonts.googleapis.com/css2?family=PT+Sans:wght@400;700&display=swap');

  html {
    font-family: 'PT Sans', sans-serif;
    letter-spacing: -0.005em;
    font-size: var(--font-size-normal);
    font-weight: var(--font-weight-normal);
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

.iconbutton.isActive {
  color: var(--color-primary);
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

.top-right-panels {
  position: fixed;
  top: var(--padding-screen);
  right: var(--padding-screen);
  display: flex;
}

.bottom-right-panels {
  position: fixed;
  bottom: var(--padding-screen);
  right: var(--padding-screen);
  display: flex;
  flex-direction: column;
}
</style>
