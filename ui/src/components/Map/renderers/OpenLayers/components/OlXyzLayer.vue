<template>
    <div v-if="false"></div>
</template>

<script>
import TileLayer from 'ol/layer/Tile'
import Projection from 'ol/proj/Projection'
import XYZSource from 'ol/source/XYZ'

const rdProjection = new Projection({
    code: 'EPSG:28992',
    extent: [-285401.92, 22598.08, 595401.92, 903401.92],
})

export default {
    name: 'OlXyzLayer',
    inject: ['map'],
    created() {
        this.tileLayer = new TileLayer({
            name: this.name,
            visible: this.isVisible,
            opacity: this.opacity,
            zIndex: this.zIndex,
            source: new XYZSource({
                url: this.url,
                projection: rdProjection,
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
        zIndex: Number,
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
