<template>
    <div v-if="false"></div>
</template>

<script>
import TileLayer from 'ol/layer/Tile'
import TileWMSSource from 'ol/source/TileWMS'

export default {
    name: 'WmsLayer',
    inject: ['map'],
    created() {
        this.source = new TileWMSSource({
            url: this.url,
            params: {
                VERSION: '1.1.1',
                FORMAT: this.format,
                LAYERS: this.name,
                tiled: true,
            },
            projection: 'EPSG:28992',
        })

        this.tileLayer = new TileLayer({
            name: this.name,
            visible: this.isVisible,
            opacity: this.opacity,
            source: this.source,
            zIndex: this.zIndex,
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
        },
        opacity(value) {
            this.tileLayer.set('opacity', value)
        },
    },
}
</script>

<style scoped></style>
