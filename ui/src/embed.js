import 'ol/ol.css'

import { register } from 'ol/proj/proj4'

import { getDefinitions } from './utils/projections'
import { getSettingsFromPath } from './utils/router'

import LayerRepository from './repository/layer'
import MapController from './map/controller'

register(getDefinitions())

const settings = getSettingsFromPath()
const layers = LayerRepository.list()

const mapController = new MapController(settings)
mapController.addLayers(layers)
mapController.render('map')
