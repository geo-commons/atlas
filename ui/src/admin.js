import 'tippy.js/themes/light-border.css'
import 'es6-promise/auto'
import 'whatwg-fetch'

import Vue from 'vue'
import VueRouter from 'vue-router'
import VueTippy, { TippyComponent } from 'vue-tippy'

import App from './admin/App'
import Dashboard from './admin/pages/Dashboard'
import Maps from './admin/pages/Maps'
import Sources from './admin/pages/Sources'
import Users from './admin/pages/Users'
import NotFound from './admin/pages/NotFound'

Vue.config.productionTip = false

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
Vue.component('tippy', TippyComponent)

const routes = [
    { path: '/', component: Dashboard, meta: { title: 'Dashboard' } },
    { path: '/maps', component: Maps, meta: { title: 'Kaarten' } },
    { path: '/sources', component: Sources, meta: { title: 'Bronnen' } },
    { path: '/users', component: Users, meta: { title: 'Gebruikers' } },
    { path: '*', component: NotFound },
]

const router = new VueRouter({
    routes,
})

// Atlas v3
document.addEventListener('DOMContentLoaded', () => {
    const el = document.querySelector('#app')
    if (!el) {
        return
    }

    new Vue({
        router,
        el: '#app',
        render: (c) => c(App),
    })
})
