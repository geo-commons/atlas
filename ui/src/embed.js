import 'ol/ol.css'
import { register } from 'ol/proj/proj4'

import { getDefinitions } from './utils/projections'
import { getSettingsFromPath } from './utils/router'
import MapController from './utils/controller'

register(getDefinitions())

const settings = getSettingsFromPath()

let layers = []
const data = document.querySelector('#layers-data')
if (data) {
  layers = JSON.parse(data.innerHTML)
}

const mapController = new MapController(settings)
mapController.addLayers(layers)
mapController.render('map')
