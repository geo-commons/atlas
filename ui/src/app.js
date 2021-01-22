import 'es6-promise/auto'
import 'whatwg-fetch'

import Vue from 'vue'
import Vuex from 'vuex'
import VueTippy, { TippyComponent } from 'vue-tippy'

import App from './pages/App'
import LegacyEmbedModal from './pages/LegacyEmbedModal'
import { createStore } from './store'
import { getSettingsFromPath } from './utils/router'

Vue.use(Vuex)
Vue.config.productionTip = false

Vue.use(VueTippy, {
  distance: 8,
  duration: [200, 175],
  hideOnClick: true,
  interactive: true,
  ignoreAttributes: true,
  allowHTML: false,
  boundary: 'window',
  delay: [1000, 0]
});

// Atlas v3
document.addEventListener('DOMContentLoaded', () => {
  const el = document.querySelector('#app')
  if (!el) {
    return
  }

  const settings = getSettingsFromPath()

  const data = JSON.parse(document.querySelector('#app-data').innerHTML)

  const layers = data.layers.map(
    (layer) => settings.visibleLayers && settings.visibleLayers.includes(layer.id) ? { ...layer, is_visible: true } : layer
  )

  const initialState = {
    position: settings.position,
    layers,
    measure: '',
    user: data.user
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
    render: (c) => c(LegacyEmbedModal),
  })
})
