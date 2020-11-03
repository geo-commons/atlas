import 'ol/ol.css'

import Vue from 'vue'
import Vuex from 'vuex'

import { register } from 'ol/proj/proj4'
import { getDefinitions } from './utils/projections'
import { getSettingsFromPath } from './utils/router'
import LayerRepository from './repository/layer'
import MapController from './map/controller'
import EmbedCode from './components/EmbedCode'

Vue.config.productionTip = false
Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    position: {
      x: 126910,
      y: 505834,
      zoom: 12.8
    },
    layers: []
  },
  mutations: {
    setPosition(state, coordinates) {
      state.position.x = coordinates.x
      state.position.y = coordinates.y
      state.position.zoom = coordinates.zoom
    },
    addLayer(state, layer) {
      const layerSet = new Set(state.layers)
      layerSet.add(layer)

      state.layers = [ ...layerSet ]
    },
    deleteLayer(state, layer) {
      const layerSet = new Set(state.layers)
      layerSet.delete(layer)

      state.layers = [ ...layerSet ]
    }
  }
})

window.vueStore = store

document.addEventListener('DOMContentLoaded', () => {
  const el = document.querySelector('#embedCode')
  if (!el) {
    return
  }

  new Vue({
    el: '#embedCode',
    store,
    render: (c) => c(EmbedCode),
  })
})

document.addEventListener('DOMContentLoaded', () => {
  const el = document.querySelector('#app')
  if (!el) {
    return
  }

  register(getDefinitions())

  const settings = getSettingsFromPath()
  const layers = LayerRepository.list()

  const mapController = new MapController(settings)
  mapController.addLayers(layers)
  mapController.render('app')
})
