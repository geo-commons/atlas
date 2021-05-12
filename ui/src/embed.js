import 'ol/ol.css'
import { register } from 'ol/proj/proj4'

import { getDefinitions } from './utils/projections'
import { getSettingsFromPath } from './utils/router'
import MapController from './utils/controller'

register(getDefinitions())

const data = JSON.parse(document.querySelector('#app-data').innerHTML)
const settings = getSettingsFromPath(data.config)

const mapController = new MapController(settings)
mapController.addLayers(data.layers)
mapController.render('map')
