import Map from 'ol/Map'
import View from 'ol/View'
import TileLayer from 'ol/layer/Tile'
import TileWMS from 'ol/source/TileWMS'
import WMTSSource from 'ol/source/WMTS'
import WMTSTileGrid from 'ol/tilegrid/WMTS'
import Projection from 'ol/proj/Projection'
import { getTopLeft } from 'ol/extent.js'

import { defaults as defaultInteractions, DragRotateAndZoom } from 'ol/interaction'

const rdProjection = new Projection({
  code: 'EPSG:28992',
  extent: [-285401.92, 22598.08, 595401.92, 903401.92]
})

// can be calculated based on resolution z0, written out for clarity
// see https://www.geonovum.nl/uploads/standards/downloads/nederlandse_richtlijn_tiling_-_versie_1.1.pdf
const resolutions = [3440.640, 1720.320, 860.160, 430.080, 215.040, 107.520, 53.760, 26.880, 13.440, 6.720, 3.360, 1.680, 0.840, 0.420, 0.210]
const matrixIds = new Array(15)
for (var i = 0; i < 15; ++i) {
  matrixIds[i] = i
}

class MapController {
  constructor(settings) {
    this.settings = settings
    this.layers = []
  }

  addLayers(layers) {
    layers.forEach((layer) => {
      this.addLayer(layer)
    })
  }

  addLayer(layer) {
    let tileLayer
    if (layer.source === 'wmts') {
      tileLayer = new TileLayer({
        id: layer.id,
        visible: (layer.is_visible === true),
        layerName: layer.name,
        opacity: layer.opacity,
        extent: rdProjection.extent,
        source: new WMTSSource({
          url: layer.url,
          layer: layer.name,
          matrixSet: 'EPSG:28992',
          format: 'image/png',
          projection: rdProjection,
          tileGrid: new WMTSTileGrid({
            origin: getTopLeft(rdProjection.getExtent()),
            resolutions,
            matrixIds
          })
        })
      })
    } else {
      tileLayer = new TileLayer({
        id: layer.id,
        visible: (layer.is_visible === true) || this.settings.visibleLayers.includes(layer.id),
        layerName: layer.name,
        opacity: layer.opacity,
        source: new TileWMS({
          projection: 'EPSG:28992',
          url: layer.url,
          servertype: layer.server_type,
          params: { 'layers': layer.name },
        })
      })
    }

    this.layers = [
      ...this.layers,
      tileLayer
    ]
  }

  render(targetId) {
    return new Map({
      interactions: defaultInteractions().extend([ new DragRotateAndZoom() ]),
      layers: this.layers,
      target: targetId,
      view: new View({
        projection: 'EPSG:28992',
        center: this.settings.position.center,
        zoom: this.settings.position.zoom
      })
    })
  }
}

export default MapController
