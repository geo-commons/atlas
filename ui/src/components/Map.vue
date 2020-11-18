<template>
    <div ref="map" class="map" />
</template>

<script>
import 'ol/ol.css'
import Map from 'ol/Map'
import View from 'ol/View'
import Feature from 'ol/Feature'
import Point from 'ol/geom/Point'
import VectorLayer from 'ol/layer/Vector'
import VectorSource from 'ol/source/Vector'
import TileLayer from 'ol/layer/Tile'
import TileWMS from 'ol/source/TileWMS'
import { Icon, Style } from 'ol/style'
import { register } from 'ol/proj/proj4'

import '../utils/projections'
import { getDefinitions } from '../utils/projections'

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

    this.map = new Map({
      target: this.$refs['map'],
      controls: [],
      layers: [
        ...this.layers.map((layer) => {
          return new TileLayer({
            id: layer.id,
            visible: layer.is_base === true,
            layerName: layer.name,
            opacity: layer.opacity,
            source: new TileWMS({
              projection: 'EPSG:28992',
              url: layer.url,
              servertype: layer.server_type,
              params: { 'layers': layer.name },
            })
          })
        }),
        this.vectorLayer
      ],
      view: new View({
        projection: 'EPSG:28992',
        center: [ this.position.center[0], this.position.center[1] ],
        zoom: this.position.zoom
      })
    })

    this.map.on('moveend', () => {
      const view = this.map.getView()

      this.$emit('set-position', {
        ...this.position,
        center: view.getCenter(),
        zoom: view.getZoom()
      })
    })

    this.map.on('singleclick', (e) => {
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
    }
  },
  props: {
    position: Object,
    layers: Array,
  }
}
</script>

<style scoped>
.map {
  width: 100%;
  height: 100%;
}
</style>
