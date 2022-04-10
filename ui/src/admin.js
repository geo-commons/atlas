import 'tippy.js/themes/light-border.css'
import 'es6-promise/auto'
import 'whatwg-fetch'

import Vue from 'vue'
import Vuex from 'vuex'
import VueRouter from 'vue-router'
import VueTippy, { TippyComponent } from 'vue-tippy'

import { createStore } from './store'
import { getSettingsFromPath } from './utils/router'
import App from './admin/App'
import Dashboard from './admin/pages/Dashboard'
import MapList from './admin/pages/MapList'
import MapCreateUpdate from './admin/pages/MapCreateUpdate'
import SourceList from './admin/pages/SourceList'
import UserList from './admin/pages/UserList'
import NotFound from './admin/pages/NotFound'

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
Vue.component('tippy', TippyComponent)

const routes = [
    { path: '/', component: Dashboard, meta: { title: 'Dashboard', menu: true } },
    { path: '/maps', component: MapList, meta: { title: 'Kaarten', menu: true } },
    { path: '/maps/create', component: MapCreateUpdate, meta: { title: 'Kaarten', menu: false } },
    {
        path: '/maps/update/:id',
        component: MapCreateUpdate,
        meta: { title: 'Kaarten', menu: false },
    },
    { path: '/sources', component: SourceList, meta: { title: 'Bronnen', menu: true } },
    { path: '/users', component: UserList, meta: { title: 'Gebruikers', menu: true } },
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

    const data = JSON.parse(document.querySelector('#app-data').innerHTML)
    const settings = getSettingsFromPath(data.config)

    const layers = data.layers.map((layer) =>
        settings.visibleLayers && settings.visibleLayers.includes(layer.id)
            ? { ...layer, is_visible: true }
            : layer
    )

    const initialState = {
        isEmbed: data.is_embed,
        config: data.config,
        position: settings.position,
        layers,
        tool: '',
        selectedArea: null,
        searchQuery: '',
        alert: '',
    }

    const store = createStore(initialState)

    new Vue({
        router,
        store,
        el: '#app',
        render: (c) => c(App),
    })
})
