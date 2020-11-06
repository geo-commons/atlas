<template>
    <div ref="map" class="map">
    </div>
</template>

<script>
import 'ol/ol.css'
import Map from 'ol/Map'
import View from 'ol/View'
import TileLayer from 'ol/layer/Tile'
import TileWMS from 'ol/source/TileWMS'
import { register } from 'ol/proj/proj4'

import '../utils/projections'
import { getDefinitions } from '../utils/projections'

// Register EPSG:28992 projection
register(getDefinitions())

let map

export default {
  name: 'Map',
  mounted() {
    map = new Map({
      target: this.$refs['map'],
      controls: [],
      layers: this.layers.map((layer) => {
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
      view: new View({
        projection: 'EPSG:28992',
        center: [ this.position.x, this.position.y ],
        zoom: this.position.zoom
      })
    })

    map.on('moveend', () => {
      const view = map.getView()
      const center = view.getCenter()

      this.$emit('set-position', {
        x: center[0],
        y: center[1],
        zoom: view.getZoom()
      })
    })
  },
  watch: {
    position(value) {
      map.getView().setCenter([ value.x, value.y ])
      map.getView().setZoom(value.zoom)
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
