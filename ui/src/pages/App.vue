<template>
  <div class="container" :style="computedStyle" :class="{ showInfoPanel: showInfoPanel && showSidePanel }">
    <PointInfoPanel :layers="this.layers" :position="this.position" @set-position="this.setPosition" :showInfoPanel="showInfoPanel && showSidePanel" @toggle-side-panel="this.toggleSidePanel" />
    <SearchPanel :position="this.position" @set-position="this.setPosition" :showInfoPanel="showInfoPanel" :showSearchPanel="showSidePanel" />
    <div class="map">
      <Map :position="this.position" :layers="this.layers" :measure="this.measure" @set-position="this.setPosition" />
      <div class="bottom-left-panels">
        <LayersPanel :layers="this.layers" @toggle-layer="this.toggleLayer" @set-layer-opacity="this.setLayerOpacity" />
      </div>
      <div class="top-right-panels">
        <MeasurePanel :measure="this.measure" @set-measure="this.setMeasure" />
        <MorePanel />
      </div>
      <div class="bottom-right-panels">
        <div class="bottom-right-wrapper">
          <div class="bottom-right-buttons" :class="{ isOpen: showBaseLayersPanel, showTogglePanorama: position.marker || showPanoramaPanel }">
            <button class="iconbutton" @click="togglePanoramaPanel" aria-label="Panorama"><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none"/><path d="M12 7C6.48 7 2 9.24 2 12c0 2.24 2.94 4.13 7 4.77V20l4-4-4-4v2.73c-3.15-.56-5-1.9-5-2.73 0-1.06 3.04-3 8-3s8 1.94 8 3c0 .73-1.46 1.89-4 2.53v2.05c3.53-.77 6-2.53 6-4.58 0-2.76-4.48-5-10-5z"/></svg></button>
            <button class="iconbutton" @click="toggleBaseLayersPanel" aria-label="Layers" :aria-expanded="showBaseLayersPanel.toString()" aria-controls="baseLayers"><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1 5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5zM10 5.47l4 1.4v11.66l-4-1.4V5.47zm-5 .99l3-1.01v11.7l-3 1.16V6.46zm14 11.08l-3 1.01V6.86l3-1.16v11.84z"/></svg></button>
          </div>
          <transition name="fade">
            <PanoramaPanel :position="this.position" :isOpen="showPanoramaPanel" @toggle="togglePanoramaPanel" />
          </transition>
          <transition name="fade">
            <BaseLayersPanel v-if="showBaseLayersPanel" :layers="this.layers" @toggle-layer="this.toggleLayer" />
          </transition>
        </div>
        <ZoomPanel :position="this.position" @set-position="this.setPosition" />
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'
import Map from '../components/Map'
import SearchPanel from '../components/SearchPanel'
import LayersPanel from '../components/LayersPanel'
import ZoomPanel from '../components/ZoomPanel'
import PanoramaPanel from '../components/PanoramaPanel'
import MorePanel from '../components/MorePanel'
import MeasurePanel from '../components/MeasurePanel'
import BaseLayersPanel from '../components/BaseLayersPanel'
import PointInfoPanel from '../components/PointInfoPanel'

export default {
  name: 'App',
  components: {
    Map,
    SearchPanel,
    LayersPanel,
    ZoomPanel,
    PanoramaPanel,
    MorePanel,
    MeasurePanel,
    BaseLayersPanel,
    PointInfoPanel,
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
    toggleLayer(values) {
      this.$store.commit('toggleLayer', values)
    },
    setLayerOpacity(values) {
      this.$store.commit('setLayerOpacity', values)
    },
    setMeasure(measure) {
      this.$store.commit('setMeasure', measure)
    },
    toggleSidePanel() {
      this.showSidePanel = !this.showSidePanel
    },
    togglePanoramaPanel() {
      this.showBaseLayersPanel = false
      this.showPanoramaPanel = !this.showPanoramaPanel
    },
    toggleBaseLayersPanel() {
      this.showPanoramaPanel = false
      this.showBaseLayersPanel = !this.showBaseLayersPanel
    },
    pushHistoryState() {
      const x = encodeURIComponent(this.position.center[0].toFixed(2))
      const y = encodeURIComponent(this.position.center[1].toFixed(2))
      const zoom = encodeURIComponent(this.position.zoom.toFixed(2))
      const layers = this.layers.filter(l => l.is_visible && !l.is_base).map(l => l.id).join(',')
      window.history.replaceState({}, '', `/atlas/v3/@${x},${y},${zoom}z/layers=${layers}`)
    }
  },
  watch: {
    position(value) {
      this.showInfoPanel = Boolean(value.marker)
      this.pushHistoryState()
    },
    layers(value) {
      this.pushHistoryState()
    }
  },
  data() {
    return {
      showInfoPanel: Boolean(this.position && this.position.marker),
      showSidePanel: true,
      showPanoramaPanel: false,
      showBaseLayersPanel: false,
      computedStyle: {
        '--color-primary': '#0066FF'
      }
    }
  }
}
</script>

<style>
  :root {
    --color-text-grey: rgba(0,0,0,.55);

    --color-grey-50: #EAEAEA;
    --color-grey-60: #DADADA;

    --font-size-small: 14px;
    --font-size-normal: 16px;

    --font-weight-normal: 400;
    --font-weight-bold: 700;

    --radius-small: 3px;
    --radius-normal: 6px;

    --shadow-normal: 0 0 1px rgba(0,0,0,.2), 0 0 8px rgba(0,0,0,.15);

    --padding-screen: 8px;

    --width-detail: 100vw;
    --width-button-normal: 32px;
    --width-button-large: 40px;
  }

  @media (min-width: 576px) {
    :root {
      --width-detail: 350px;
    }
  }

  @media (min-width: 992px) {
    :root {
      --padding-screen: 16px;
    }
  }

  @media (min-width: 1200px) {
    :root {
      --padding-screen: 20px;
    }
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
  text-align: left;
}

input::placeholder {
  color: var(--color-text-grey);
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

svg {
  flex-shrink: 0;
}

.iconbutton {
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-radius .1s;
}

.iconbutton[disabled] {
  color: var(--color-grey-60);
}

.iconbutton.isActive {
  color: var(--color-primary);
}

.counter {
  flex-shrink: 0;
  height: 18px;
  min-width: 18px;
  border-radius: 9px;
  border: 2px solid var(--color-primary);
  padding: 0 3px;
  background: white;
  color: var(--color-primary);
  font-size: 11px;
  font-weight: var(--font-weight-bold);
  line-height: 14px;
  text-align: center;
  white-space: nowrap;
  user-select: none;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .1s;
}
.fade-enter, .fade-leave-to {
  opacity: 0;
}
</style>

<style scoped>
.container {
  width: 100%;
  height: 100%;
  display: flex;
}

.map {
  position: relative;
  flex-grow: 1;
}

.bottom-left-panels {
  position: absolute;
  bottom: var(--padding-screen);
  left: var(--padding-screen);
}

@media (min-width: 576px) {
  .showInfoPanel .bottom-left-panels {
    left: calc(var(--padding-screen) + var(--width-detail));
  }
}

.top-right-panels {
  position: absolute;
  top: calc((var(--padding-screen) * 2) + var(--width-button-large));
  right: var(--padding-screen);
  display: flex;
}

@media (min-width: 576px) {
  .top-right-panels {
    top: var(--padding-screen);
  }
}

.bottom-right-panels {
  position: absolute;
  bottom: var(--padding-screen);
  right: var(--padding-screen);
  display: flex;
  flex-direction: column;
}

.bottom-right-wrapper {
  position: relative;
  margin-bottom: 12px;
}

.bottom-right-buttons {
  display: flex;
  flex-direction: column;
  justify-content: flex-end;
  background: white;
  border-radius: var(--radius-normal);
  overflow: hidden;
  box-shadow: var(--shadow-normal);
  height: var(--width-button-normal);
  transition: height .1s ease, border-radius .1s;
  overflow: hidden;
}

.bottom-right-buttons.isOpen {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.bottom-right-buttons.showTogglePanorama {
  height: calc(var(--width-button-normal) * 2 + 1px);
}

.bottom-right-buttons .iconbutton {
  width: var(--width-button-normal);
  height: var(--width-button-normal);
}

.bottom-right-buttons .iconbutton:first-child {
  box-sizing: content-box;
  border-bottom: 1px solid #EAEAEA;
}
</style>
