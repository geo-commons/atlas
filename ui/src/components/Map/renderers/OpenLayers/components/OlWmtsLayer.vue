<template>
    <div v-if="false"></div>
</template>

<script>
import TileLayer from 'ol/layer/Tile'
import WMTSCapabilities from 'ol/format/WMTSCapabilities'
import WMTSSource, { optionsFromCapabilities } from 'ol/source/WMTS'

export default {
    name: 'WmtsLayer',
    inject: ['map'],
    created() {
        this.tileLayer = new TileLayer({
            name: this.name,
            visible: this.isVisible,
            opacity: this.opacity,
            source: null,
            zIndex: this.zIndex,
        })

        this.map.addLayer(this.tileLayer)

        if (this.isVisible) {
            this.setSource()
        }
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
        zIndex: Number,
        format: String,
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

            if (value && !this.tileLayer.getSource()) {
                this.setSource()
            }
        },
        opacity(value) {
            this.tileLayer.set('opacity', value)
        },
    },
    methods: {
        async setSource() {
            const response = await fetch(`${this.url}?REQUEST=GetCapabilities&service=wmts`)
            const body = await response.text()
            const caps = new WMTSCapabilities().read(body)
            const wmts = new WMTSSource(
                optionsFromCapabilities(caps, {
                    layer: this.name,
                    matrixSet: 'EPSG:28992',
                    format: this.format,
                })
            )

            this.tileLayer.setSource(
                new WMTSSource({
                    url: this.url,
                    layer: this.name,
                    projection: 'EPSG:28992',
                    matrixSet: 'EPSG:28992',
                    format: this.format,
                    tileGrid: wmts.getTileGrid(),
                })
            )
        },
    },
}
</script>

<style scoped></style>
