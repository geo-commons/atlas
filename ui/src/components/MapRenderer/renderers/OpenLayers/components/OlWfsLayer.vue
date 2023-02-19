<template>
    <div v-if="false"></div>
</template>

<script>
import VectorLayer from 'ol/layer/Vector'
import { bbox as bboxStrategy } from 'ol/loadingstrategy'
import GeoJSON from 'ol/format/GeoJSON'
import VectorSource from 'ol/source/Vector'
import { Style, Fill, Stroke, Circle } from 'ol/style'
import OpenLayersParser from 'geostyler-openlayers-parser'

const olParser = new OpenLayersParser()

const DEFAULT_STYLE = [
    new Style({
        stroke: new Stroke({
            color: 'blue',
            width: 3,
        }),
        fill: new Fill({
            color: 'rgba(0, 0, 255, 0.1)',
        }),
    }),
    new Style({
        image: new Circle({
            radius: 10,
            fill: new Fill({
                color: 'blue',
            }),
        }),
    }),
]

export default {
    name: 'WfsLayer',
    inject: ['map'],
    created() {
        this.source = new VectorSource({
            format: new GeoJSON(),
            strategy: bboxStrategy,
            url: (extent) => {
                const params = new URLSearchParams([
                    ['service', 'WFS'],
                    ['version', '1.0.0'],
                    ['request', 'GetFeature'],
                    ['typename', this.name],
                    ['outputFormat', 'application/json'],
                    ['srsname', 'EPSG:28992'],
                    ['bbox', extent.join(',')],
                ])

                const url = new URL(this.url)
                url.search = params.toString()

                return url.toString()
            },
        })

        this.tileLayer = new VectorLayer({
            name: this.name,
            visible: this.isVisible,
            source: this.source,
            opacity: this.opacity,
            zIndex: this.zIndex,
            selectable: true,
        })

        this.map.addLayer(this.tileLayer)
        this.applyStyle(this.vectorStyle)
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
        vectorStyle: Object,
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
        vectorStyle(value) {
            this.applyStyle(value)
        },
    },
    methods: {
        async applyStyle(inputStyle) {
            if (!inputStyle) {
                return this.tileLayer.setStyle(DEFAULT_STYLE)
            }

            try {
                const olStyle = await olParser.writeStyle(inputStyle)
                this.tileLayer.setStyle(olStyle.output)
            } catch (e) {
                console.error('Unable to parse style', e)
            }
        },
    },
}
</script>

<style scoped></style>
