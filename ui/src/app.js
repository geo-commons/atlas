import 'es6-promise/auto'
import 'whatwg-fetch'

import Vue from 'vue'
import Vuex from 'vuex'

import App from './pages/App'
import EmbedCode from './components/EmbedCode'
import { createStore } from './store'
import { getSettingsFromPath } from './utils/router'

Vue.use(Vuex)
Vue.config.productionTip = false

// Atlas v3
document.addEventListener('DOMContentLoaded', () => {
  const el = document.querySelector('#app')
  if (!el) {
    return
  }

  const settings = getSettingsFromPath()

  const layers = JSON.parse(document.querySelector('#layers-data').innerHTML).map(
    (layer) => settings.visibleLayers && settings.visibleLayers.includes(layer.id) ? { ...layer, is_visible: true } : layer
  )

  const initialState = {
    position: settings.position,
    layers,
    measure: ''
  }

  const store = createStore(initialState)

  new Vue({
    el: '#app',
    store,
    render: (c) => c(App),
  })
})

// Embed map in jQuery frontend
document.addEventListener('DOMContentLoaded', () => {
  const el = document.querySelector('#embedCode')
  if (!el) {
    return
  }

  const settings = getSettingsFromPath()

  const initialState = {
    position: settings.position,
    layers: [],
    measure: ''
  }

  const store = createStore(initialState)
  window.vueStore = store // assign store to window for interoperability with old jQuery frontend

  new Vue({
    el: '#embedCode',
    store,
    render: (c) => c(EmbedCode),
  })
})
