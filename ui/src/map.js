import 'tippy.js/themes/light-border.css'
import 'es6-promise/auto'
import 'whatwg-fetch'

import Vue from 'vue'
import VueTippy, { TippyComponent } from 'vue-tippy'

import { getSettingsFromPath } from './utils/router'
import Map from './components/Map/Map'

Vue.config.productionTip = false

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

// Atlas v3
document.addEventListener('DOMContentLoaded', () => {
    const el = document.querySelector('#map')
    if (!el) {
        return
    }

    const data = JSON.parse(document.querySelector('#map-data').innerHTML)
    const settings = getSettingsFromPath(data.config)

    const layers = data.layers.map((layer) => {
        return { ...layer, is_visible: true }
    })

    new Vue({
        el: '#map',
        render: (c) =>
            c(Map, {
                props: {
                    initialPosition: settings.position,
                    initialLayers: layers,
                    user: data.user,
                    features: data.features,
                    settings: data.settings,
                },
            }),
    })
})
