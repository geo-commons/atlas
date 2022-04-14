<template>
    <div v-if="false"></div>
</template>

<script>
import TileLayer from 'ol/layer/Tile'
import Projection from 'ol/proj/Projection'
import WMTSTileGrid from 'ol/tilegrid/WMTS'
import WMTSSource from 'ol/source/WMTS'
import { getTopLeft } from 'ol/extent.js'

const rdProjection = new Projection({
    code: 'EPSG:28992',
    extent: [-285401.92, 22598.08, 595401.92, 903401.92],
})

// can be calculated based on resolution z0, written out for clarity
// see https://www.geonovum.nl/uploads/standards/downloads/nederlandse_richtlijn_tiling_-_versie_1.1.pdf
const resolutions = [
    3440.64, 1720.32, 860.16, 430.08, 215.04, 107.52, 53.76, 26.88, 13.44, 6.72, 3.36, 1.68, 0.84,
    0.42, 0.21,
]

const matrixIds = new Array(15)
for (var i = 0; i < 15; ++i) {
    matrixIds[i] = i
}

export default {
    name: 'WmtsLayer',
    inject: ['map'],
    created() {
        this.tileLayer = new TileLayer({
            name: this.name,
            visible: this.isVisible,
            opacity: this.opacity,
            source: new WMTSSource({
                url: this.url,
                layer: this.name,
                projection: rdProjection,
                matrixSet: 'EPSG:28992',
                format: 'image/png',
                tileGrid: new WMTSTileGrid({
                    origin: getTopLeft(rdProjection.getExtent()),
                    resolutions,
                    matrixIds,
                }),
            }),
        })

        this.map.addLayer(this.tileLayer)
    },
    destroyed() {
        this.map.removeLayer(this.tileLayer)
    },
    props: {
        name: String,
        url: String,
        layer: String,
        isVisible: Boolean,
        opacity: Number,
    },
    watch: {
        url(value) {
            this.source.set('url', value)
        },
        name(value) {
            this.tileLayer.set('name', value)
        },
        isVisible(value) {
            this.tileLayer.set('visible', value)
        },
        opacity(value) {
            this.tileLayer.set('opacity', value)
        },
    },
}
</script>

<style scoped></style>
