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
import WMTSSource from 'ol/source/WMTS'
import WMTSTileGrid from 'ol/tilegrid/WMTS'
import Projection from 'ol/proj/Projection'
import { getTopLeft } from 'ol/extent.js'
import { register } from 'ol/proj/proj4'

import { getDefinitions } from '../utils/projections'
import constructDraw from '../utils/draw'
import getMarkerUrl from '../utils/generate-marker-url'

// Register EPSG:28992 projection
register(getDefinitions())

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
    name: 'Map',
    mounted() {
        this.markerSource = new VectorSource()
        this.markerLayer = new VectorLayer({
            source: this.markerSource,
        })

        this.selectedAreaSource = new VectorSource()
        this.selectedAreaLayer = new VectorLayer({
            source: this.selectedAreaSource,
        })

        if (this.position.marker) {
            const markerFeature = new Feature({
                geometry: new Point([this.position.marker[0], this.position.marker[1]]),
            })

            const markerStyle = new Style({
                image: new Icon({
                    src: getMarkerUrl('#0066FF', '#FFFFFF'),
                    anchor: [0.55, 42],
                    anchorXUnits: 'fraction',
                    anchorYUnits: 'pixels',
                }),
            })

            markerFeature.setStyle(markerStyle)
            this.markerSource.addFeature(markerFeature)
        }

        this.tileLayers = {}

        this.view = new View({
            projection: 'EPSG:28992',
            center: [this.position.center[0], this.position.center[1]],
            zoom: this.position.zoom,
            padding: this.padding,
        })

        this.map = new Map({
            target: this.$refs['map'],
            controls: [],
            layers: [
                ...this.layers.map((layer) => {
                    let tileLayer
                    if (layer.source_type === 'WMTS') {
                        tileLayer = new TileLayer({
                            id: layer.id,
                            visible: layer.is_visible === true,
                            layerName: layer.name,
                            opacity: layer.opacity,
                            extent: rdProjection.extent,
                            source: new WMTSSource({
                                url: layer.url,
                                layer: layer.name,
                                matrixSet: layer.projection,
                                format: 'image/png',
                                projection: rdProjection,
                                tileGrid: new WMTSTileGrid({
                                    origin: getTopLeft(rdProjection.getExtent()),
                                    resolutions,
                                    matrixIds,
                                }),
                            }),
                        })
                    } else {
                        tileLayer = new TileLayer({
                            id: layer.id,
                            visible: layer.is_visible === true,
                            layerName: layer.name,
                            opacity: layer.opacity,
                            source: new TileWMS({
                                projection: 'EPSG:28992',
                                url: layer.url,
                                servertype: layer.server_type,
                                params: { layers: layer.name },
                            }),
                        })
                    }

                    this.tileLayers[layer.id] = tileLayer
                    return tileLayer
                }),
                this.markerLayer,
                this.selectedAreaLayer,
            ],
            view: this.view,
        })

        if (this.tool !== '') {
            const onDrawStart = () => {
                this.selectedAreaSource.clear()
            }

            const onDrawEnd = (sketch) => {
                this.$emit('tool-used', { tool: this.tool, sketch })
            }

            this.draw = constructDraw(this.tool, onDrawStart, onDrawEnd)
            this.map.addInteraction(this.draw)
        }

        this.map.on('moveend', () => {
            const view = this.map.getView()

            this.$emit('set-position', {
                ...this.position,
                center: view.getCenter(),
                zoom: view.getZoom(),
            })
        })

        this.map.on('singleclick', (e) => {
            if (this.tool !== '') {
                return
            }

            this.$emit('set-position', {
                ...this.position,
                marker: e.coordinate,
            })
        })
    },
    watch: {
        position(value, oldValue) {
            const view = this.map.getView()

            if (value.center != oldValue.center) {
                view.setCenter(value.center)
            }

            if (value.zoom != oldValue.zoom) {
                view.animate({
                    zoom: value.zoom,
                    duration: 250,
                })
            }

            this.markerSource.clear()
            if (value.marker) {
                const markerFeature = new Feature({
                    geometry: new Point([this.position.marker[0], this.position.marker[1]]),
                })

                const markerStyle = new Style({
                    image: new Icon({
                        src: getMarkerUrl('#0066FF', '#FFFFFF'),
                        anchor: [0.55, 42],
                        anchorXUnits: 'fraction',
                        anchorYUnits: 'pixels',
                    }),
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
                this.$emit('tool-used', { tool: value, sketch })
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
                    fill: new Fill({ color: 'rgba(0, 102, 255, 0.2)' }),
                })

                selectedAreaFeature.setStyle(selectedAreaStyle)
                this.selectedAreaSource.addFeature(selectedAreaFeature)
            }
        },
        padding(value) {
            this.view.setProperties({ padding: value })
        },
    },
    props: {
        position: Object,
        layers: Array,
        tool: String,
        selectedArea: Object,
        padding: { type: Array, default: () => [0, 0, 0, 0] },
    },
}
</script>

<style scoped>
.wrapper {
    width: 100%;
    height: 100%;
}
</style>
