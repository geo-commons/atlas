import Vue from 'vue'
import Vuex from 'vuex'

Vue.use(Vuex)

const store = new Vuex.Store({
  state: {
    position: {
      x: 126910,
      y: 505834,
      zoom: 13
    },
    layers: document.querySelector('#layers-data') ? JSON.parse(document.querySelector('#layers-data').innerHTML) : []
  },
  mutations: {
    setPosition(state, position) {
      state.position = position
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
    },
  }
})

window.vueStore = store // assign store to window for interoperability with old jQuery frontend

export default store
