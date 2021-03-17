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
import { Icon, Style, Fill, Stroke, Text } from 'ol/style'
import { register } from 'ol/proj/proj4'

import { getDefinitions } from '../utils/projections'
import constructDraw from '../utils/draw'
import getMarkerUrl from "../utils/generate-marker-url"

// Register EPSG:28992 projection
register(getDefinitions())

export default {
  name: 'Map',
  mounted() {
    this.markerSource = new VectorSource()
    this.markerLayer = new VectorLayer({
      source: this.markerSource
    })

    this.selectedAreaSource = new VectorSource()
    this.selectedAreaLayer = new VectorLayer({
      source: this.selectedAreaSource
    })

    if (this.position.marker) {
      const markerFeature = new Feature({
        geometry: new Point([ this.position.marker[0], this.position.marker[1] ]),
      })

      const markerStyle = new Style({
        image: new Icon({
          src: getMarkerUrl("#0066FF", "#FFFFFF"),
          anchor: [ 0.55, 42 ],
          anchorXUnits: 'fraction',
          anchorYUnits: 'pixels',
        })
      })

      markerFeature.setStyle(markerStyle)
      this.markerSource.addFeature(markerFeature)
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
        this.markerLayer,
        this.selectedAreaLayer
      ],
      view: new View({
        projection: 'EPSG:28992',
        center: [ this.position.center[0], this.position.center[1] ],
        zoom: this.position.zoom
      })
    })

    if (this.tool !== '') {
      const onDrawStart = () => {
        this.selectedAreaSource.clear()
      }

      const onDrawEnd = (sketch) => {
        this.$emit('tool-used', { 'tool': this.tool, sketch })
      }

      this.draw = constructDraw(this.tool, onDrawStart, onDrawEnd)
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
      this.markerSource.clear()

      if (value.marker) {
        const markerFeature = new Feature({
          geometry: new Point([ this.position.marker[0], this.position.marker[1] ]),
        })

        const markerStyle = new Style({
          image: new Icon({
            src: getMarkerUrl("#0066FF", "#FFFFFF"),
            anchor: [ 0.55, 42 ],
            anchorXUnits: 'fraction',
            anchorYUnits: 'pixels',
          })
        })

        markerFeature.setStyle(markerStyle)
        this.markerSource.addFeature(markerFeature)
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

      const onDrawStart = () => {
        this.selectedAreaSource.clear()
      }

      const onDrawEnd = (sketch) => {
        this.$emit('tool-used', { 'tool': value, sketch })
      }

      if (value !== '') {
        this.draw = constructDraw(value, onDrawStart, onDrawEnd)
        this.map.addInteraction(this.draw)
      }
    },
    selectedArea(selectedArea) {
      this.selectedAreaSource.clear()

      if (selectedArea) {
        const selectedAreaFeature = new Feature({
          geometry: selectedArea,
        })

        const selectedAreaStyle = new Style({
          stroke: new Stroke({ color: 'rgba(0, 102, 255, 1)' }),
          fill: new Fill({ color: 'rgba(0, 102, 255, 0.2)' })
        })

        selectedAreaFeature.setStyle(selectedAreaStyle)
        this.selectedAreaSource.addFeature(selectedAreaFeature)
      }
    }
  },
  props: {
    position: Object,
    layers: Array,
    tool: String,
    selectedArea: Object
  }
}
</script>

<style scoped>
.wrapper {
  width: 100%;
  height: 100%;
}
</style>
