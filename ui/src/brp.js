import 'tippy.js/themes/light-border.css'
import 'es6-promise/auto'
import 'whatwg-fetch'

import Vue from 'vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import VueTippy, { TippyComponent } from 'vue-tippy'

import App from './brp/App'
import Index from './brp/pages/Index'

Vue.config.productionTip = false

Vue.use(Vuex)
Vue.use(VueRouter)
Vue.use(VueTippy, {
    directive: 'tippy',
    distance: 5,
    placement: 'top',
    duration: [200, 175],
    hideOnClick: true,
    interactive: true,
    ignoreAttributes: true,
    allowHTML: false,
    boundary: 'viewport',
    delay: [1000, 0],
})
Vue.component('VueTippy', TippyComponent)

const routes = [
    { path: '/', component: Index, meta: { title: 'Overzicht', menu: true } },
]

const router = new VueRouter({
    routes,
})

document.addEventListener('DOMContentLoaded', () => {
    const el = document.querySelector('#app')
    if (!el) {
        return
    }

    //const data = JSON.parse(document.querySelector('#app-data').innerHTML)

    new Vue({
        router,
        el: '#app',
        render: (c) => c(App),
    })
})
