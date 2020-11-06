import Vue from 'vue'

import store from './store'
import App from './pages/App'
import EmbedCode from './components/EmbedCode'

Vue.config.productionTip = false

// Atlas v3
document.addEventListener('DOMContentLoaded', () => {
  const el = document.querySelector('#app')
  if (!el) {
    return
  }

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

  new Vue({
    el: '#embedCode',
    store,
    render: (c) => c(EmbedCode),
  })
})
