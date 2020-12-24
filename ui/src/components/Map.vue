<template>
    <div ref="map" class="wrapper" />
</template>

<script>
import 'ol/ol.css'
import Map from 'ol/Map'

import View from 'ol/View'
import Feature from 'ol/Feature'
import { Point } from 'ol/geom'
import VectorLayer from 'ol/layer/Vector'
import VectorSource from 'ol/source/Vector'
import TileLayer from 'ol/layer/Tile'
import TileWMS from 'ol/source/TileWMS'
import { Icon, Style } from 'ol/style'
import { register } from 'ol/proj/proj4'

import { getDefinitions } from '../utils/projections'
import constructDraw from '../utils/draw'

// Register EPSG:28992 projection
register(getDefinitions())

export default {
  name: 'Map',
  mounted() {
    this.vectorSource = new VectorSource()
    this.vectorLayer = new VectorLayer({
      source: this.vectorSource
    })

    if (this.position.marker) {
      const markerFeature = new Feature({
        geometry: new Point([ this.position.marker[0], this.position.marker[1] ]),
      })

      const markerStyle = new Style({
        image: new Icon({
          anchor: [ 0.5, 46 ],
          anchorXUnits: 'fraction',
          anchorYUnits: 'pixels',
          src: '/atlas/static/img/icon.png'
        })
      })

      markerFeature.setStyle(markerStyle)
      this.vectorSource.addFeature(markerFeature)
    }

    this.tileLayers = {}

    this.map = new Map({
      target: this.$refs['map'],
      controls: [],
      layers: [
        ...this.layers.map((layer) => {
          const tileLayer = new TileLayer({
            id: layer.id,
            visible: (layer.is_visible === true),
            layerName: layer.name,
            opacity: layer.opacity,
            source: new TileWMS({
              projection: 'EPSG:28992',
              url: layer.url,
              servertype: layer.server_type,
              params: { 'layers': layer.name },
            })
          })

          this.tileLayers[layer.id] = tileLayer
          return tileLayer
        }),
        this.vectorLayer
      ],
      view: new View({
        projection: 'EPSG:28992',
        center: [ this.position.center[0], this.position.center[1] ],
        zoom: this.position.zoom
      })
    })

    if (this.tool !== '') {
      this.draw = constructDraw(this.tool)
      this.map.addInteraction(this.draw)
    }

    this.map.on('moveend', () => {
      const view = this.map.getView()

      this.$emit('set-position', {
        ...this.position,
        center: view.getCenter(),
        zoom: view.getZoom()
      })
    })

    this.map.on('singleclick', (e) => {
      if (this.tool !== '') {
        // do not interact on click when a tool like measuring or selecting is enabled
        return
      }

      this.$emit('set-position', {
        ...this.position,
        marker: e.coordinate
      })
    })
  },
  watch: {
    position(value) {
      this.map.getView().setCenter(value.center)
      this.map.getView().setZoom(value.zoom)
      this.vectorSource.clear()

      if (value.marker) {
        const markerFeature = new Feature({
          geometry: new Point([ this.position.marker[0], this.position.marker[1] ]),
        })

        const markerStyle = new Style({
          image: new Icon({
            anchor: [ 0.5, 46 ],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
            src: '/atlas/static/img/icon.png'
          })
        })

        markerFeature.setStyle(markerStyle)
        this.vectorSource.addFeature(markerFeature)
      }
    },
    layers(value) {
      value.forEach((layer) => {
        if (layer.is_visible !== this.tileLayers[layer.id].getVisible()) {
          this.tileLayers[layer.id].setVisible(layer.is_visible)
        }
        if (layer.opacity !== this.tileLayers[layer.id].getOpacity()) {
          this.tileLayers[layer.id].setOpacity(layer.opacity)
        }
      })
    },
    tool(value) {
      this.map.removeInteraction(this.draw)

      const onDrawEnd = (sketch) => {
        this.$emit('tool-used', { 'tool': value, sketch })
      }

      switch(value) {
        case 'MEASURE_LINE':
          this.draw = constructDraw('line', onDrawEnd)
          this.map.addInteraction(this.draw)
          break
        case 'MEASURE_AREA':
        case 'SELECT_AREA':
          this.draw = constructDraw('area', onDrawEnd)
          this.map.addInteraction(this.draw)
          break
        case '':
          break
        default:
          console.error('Tried to activate an unknown tool: ', value)
      }
    }
  },
  props: {
    position: Object,
    layers: Array,
    tool: String
  }
}
</script>

<style scoped>
.wrapper {
  width: 100%;
  height: 100%;
}
</style>
