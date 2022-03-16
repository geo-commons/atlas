<template>
    <div ref="map" class="map">
        <!-- Move to ui-container? -->
        <div class="scale" @click="this.toggleScaleType">
            <div
                ref="scale-line-container"
                :style="{ display: this.scaleType === 'LINE' ? 'block' : 'none' }"
            />
            <div
                class="scale-text"
                :style="{ display: this.scaleType === 'TEXT' ? 'block' : 'none' }"
            >
                1 : {{ Math.round(scale).toLocaleString() }}
            </div>
        </div>
    </div>
</template>

<script>
import 'ol/ol.css'
import Map from 'ol/Map'

import View from 'ol/View'
import Feature from 'ol/Feature'
import { Point } from 'ol/geom'
import ScaleLine from 'ol/control/ScaleLine'
import VectorLayer from 'ol/layer/Vector'
import VectorSource from 'ol/source/Vector'
import TileLayer from 'ol/layer/Tile'
import TileWMS from 'ol/source/TileWMS'
import XYZ from 'ol/source/XYZ'
import { Icon, Style, Fill, Stroke, Circle } from 'ol/style'
import WMTSCapabilities from 'ol/format/WMTSCapabilities'
import WMTSSource, { optionsFromCapabilities } from 'ol/source/WMTS'
import WMTSTileGrid from 'ol/tilegrid/WMTS'
import VectorTileLayer from 'ol/layer/VectorTile'
import VectorTileSource from 'ol/source/VectorTile'
import GeoJSON from 'ol/format/GeoJSON'
import MVT from 'ol/format/MVT'
import Projection from 'ol/proj/Projection'
import { getPointResolution } from 'ol/proj'
import { bbox as bboxStrategy } from 'ol/loadingstrategy'
import { getTopLeft } from 'ol/extent.js'
import { register } from 'ol/proj/proj4'

import { getDefinitions } from '../utils/projections'
import constructDraw from '../utils/draw'
import getMarkerIconUrl from '../utils/generate-marker-icon-url'
import getLocationIconUrl from '../utils/generate-location-icon-url'

import OpenLayersParser from 'geostyler-openlayers-parser'
const olParser = new OpenLayersParser()

// Register EPSG:28992 projection
register(getDefinitions())

const rdProjection = new Projection({
    code: 'EPSG:28992',
    extent: [-285401.92, 22598.08, 595401.92, 903401.92],
})

const DEFAULT_DPI = 25.4 / 0.28

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

        this.geolocationSource = new VectorSource()
        this.geolocationLayer = new VectorLayer({
            source: this.geolocationSource,
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

        if (this.position.geolocation) {
            const geolocationFeature = new Feature({
                geometry: new Point([this.position.geolocation[0], this.position.geolocation[1]]),
            })

            const geolocationStyle = new Style({
                image: new Icon({
                    src: getMarkerUrl('#0066FF', '#FFFFFF'),
                    anchor: [0.55, 42],
                    anchorXUnits: 'fraction',
                    anchorYUnits: 'pixels',
                }),
            })

            geolocationFeature.setStyle(geolocationStyle)
            this.markerSource.addFeature(geolocationFeature)
        }

        this.tileLayers = {}

        this.view = new View({
            projection: 'EPSG:28992',
            constrainResolution: true,
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
                    } else if (layer.source_type === 'XYZ') {
                        tileLayer = new TileLayer({
                            id: layer.id,
                            visible: layer.is_visible === true,
                            layerName: layer.name,
                            opacity: layer.opacity,
                            source: new XYZ({
                                projection:
                                    layer.projection === 'EPSG:28992' ? rdProjection : 'EPSG:3857',
                                url: layer.url,
                            }),
                        })
                    } else if (layer.source_type === 'WFS') {
                        tileLayer = new VectorLayer({
                            id: layer.id,
                            visible: layer.is_visible === true,
                            layerName: layer.name,
                            opacity: layer.opacity,
                            source: new VectorSource({
                                format: new GeoJSON(),
                                url: (extent) => {
                                    const params = new URLSearchParams([
                                        ['service', 'WFS'],
                                        ['version', '1.0.0'],
                                        ['request', 'GetFeature'],
                                        ['typename', layer.name],
                                        ['outputFormat', 'application/json'],
                                        ['srsname', layer.projection],
                                        ['bbox', extent.join(',')],
                                    ])

                                    return layer.url + params.toString()
                                },
                                strategy: bboxStrategy,
                            }),
                            style: () => {
                                if (layer.style) {
                                    olParser
                                        .writeStyle(layer.style)
                                        .then((olStyle) =>
                                            this.tileLayers[layer.id].setStyle(olStyle.output)
                                        )
                                        .catch((error) => console.error(error))
                                }

                                return [
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
                            },
                        })
                    } else if (layer.source_type === 'MVT') {
                        tileLayer = new VectorTileLayer({
                            id: layer.id,
                            visible: layer.is_visible === true,
                            layerName: layer.name,
                            opacity: layer.opacity,
                            source: null,
                            style: () => {
                                if (layer.style) {
                                    olParser
                                        .writeStyle(layer.style)
                                        .then((olStyle) =>
                                            this.tileLayers[layer.id].setStyle(olStyle.output)
                                        )
                                        .catch((error) => console.error(error))
                                } else {
                                    return [
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
                                }
                            },
                        })

                        fetch(`${layer.url}?REQUEST=GetCapabilities`, this.getFetchParameters())
                            .then((response) => {
                                return response.text()
                            })
                            .then((body) => {
                                const caps = new WMTSCapabilities().read(body)
                                const wmts = new WMTSSource(
                                    optionsFromCapabilities(caps, {
                                        layer: layer.name,
                                        matrixSet: 'EPSG:28992',
                                        format: 'application/vnd.mapbox-vector-tile',
                                    })
                                )

                                tileLayer.setSource(
                                    new VectorTileSource({
                                        projection: 'EPSG:28992',
                                        format: new MVT(),
                                        tileGrid: wmts.getTileGrid(),
                                        tileUrlFunction: wmts.getTileUrlFunction(),
                                        tileLoadFunction: (tile, url) => {
                                            tile.setLoader((extent, resolution, projection) => {
                                                fetch(url, this.getFetchParameters()).then(
                                                    (response) => {
                                                        response.arrayBuffer().then((data) => {
                                                            const format = tile.getFormat()
                                                            const features = format.readFeatures(
                                                                data,
                                                                {
                                                                    extent: extent,
                                                                    featureProjection: projection,
                                                                }
                                                            )
                                                            tile.setFeatures(features)
                                                        })
                                                    }
                                                )
                                            })
                                        },
                                    })
                                )
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
                                tileLoadFunction: (tile, src) => {
                                    if (!this.user || !this.user.token) {
                                        tile.getImage().src = src
                                        return
                                    }

                                    const xhr = new XMLHttpRequest()
                                    xhr.responseType = 'blob'
                                    xhr.addEventListener('loadend', function (evt) {
                                        const data = this.response
                                        if (data !== undefined) {
                                            tile.getImage().src = URL.createObjectURL(data)
                                        } else {
                                            tile.setState(TileState.ERROR)
                                        }
                                    })
                                    xhr.addEventListener('error', function () {
                                        tile.setState(TileState.ERROR)
                                    })
                                    xhr.open('GET', src)

                                    xhr.setRequestHeader(
                                        'Authorization',
                                        `Bearer ${this.user.token}`
                                    )

                                    xhr.send()
                                },
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

            this.draw = constructDraw(this.tool, this.map, onDrawStart, onDrawEnd)
            this.map.addInteraction(this.draw)
        }

        this.map.on('pointermove', (e) => {
            if (e.dragging) {
                return
            }

            const pixel = this.map.getEventPixel(e.originalEvent)
            const hit = this.map.hasFeatureAtPixel(pixel)
            this.map.getTarget().style.cursor = hit ? 'pointer' : ''
        })

        this.map.on('moveend', () => {
            const view = this.map.getView()

            const resolution = getPointResolution(
                this.view.getProjection(),
                this.view.getResolution(),
                this.view.getCenter()
            )

            const mpu = this.view.getProjection().getMetersPerUnit()
            const inchesPerMeter = 1000 / 25.4
            this.scale = parseFloat(resolution.toString()) * mpu * inchesPerMeter * DEFAULT_DPI

            this.$emit('set-position', {
                ...this.position,
                center: view.getCenter(),
                zoom: view.getZoom(),
                extent: view.calculateExtent(this.map.getSize()),
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

        this.scaleline = new ScaleLine({
            text: true,
            target: this.$refs['scale-line-container'],
            className: 'scale-line',
        })

        this.map.addControl(this.scaleline)
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
                        src: getMarkerIconUrl('#0066FF', '#FFFFFF'),
                        anchor: [0.55, 42],
                        anchorXUnits: 'fraction',
                        anchorYUnits: 'pixels',
                    }),
                })

                markerFeature.setStyle(markerStyle)
                this.markerSource.addFeature(markerFeature)
            }

            this.geolocationSource.clear()
            if (value.geolocation) {
                const geolocationFeature = new Feature({
                    geometry: new Point([
                        this.position.geolocation[0],
                        this.position.geolocation[1],
                    ]),
                })

                const geolocationStyle = new Style({
                    image: new Icon({
                        src: getLocationIconUrl('#0066FF', '#FFFFFF'),
                        anchor: [0.55, 42],
                        anchorXUnits: 'fraction',
                        anchorYUnits: 'pixels',
                    }),
                })

                geolocationFeature.setStyle(geolocationStyle)
                this.markerSource.addFeature(geolocationFeature)
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
                this.draw = constructDraw(value, this.map, onDrawStart, onDrawEnd)
                this.map.addInteraction(this.draw)
            }

            if (value === '') {
                this.selectedAreaSource.clear()
                this.map.removeOverlay(this.draw.measureTooltip)
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
    methods: {
        toggleScaleType() {
            this.scaleType = this.scaleType === 'LINE' ? 'TEXT' : 'LINE'
        },
        fit(geometryOrExtent, options) {
            this.view.fit(geometryOrExtent, options)
        },
        getFetchParameters() {
            if (this.user && this.user.token) {
                return {
                    headers: { Authorization: `Bearer ${this.user.token}` },
                }
            }

            return {}
        },
    },
    data() {
        return {
            scaleType: 'LINE',
            scale: 0,
        }
    },
    props: {
        position: Object,
        layers: Array,
        tool: String,
        selectedArea: Object,
        user: Object,
        padding: { type: Array, default: () => [0, 0, 0, 0] },
    },
}
</script>

<style scoped>
.map >>> .ol-tooltip {
    position: relative;
    background: rgba(0, 0, 0, 0.5);
    border-radius: 4px;
    color: white;
    padding: 4px 8px;
    opacity: 0.7;
    white-space: nowrap;
    font-size: 12px;
    cursor: default;
    user-select: none;
}

.map >>> .ol-tooltip-measure {
    opacity: 1;
    font-weight: bold;
}

.map >>> .ol-tooltip-static {
    background-color: #000000;
    color: white;
    border: 1px solid white;
}

.map >>> .ol-tooltip-measure:before,
.map >>> .ol-tooltip-static:before {
    border-top: 6px solid rgba(0, 0, 0, 0.5);
    border-right: 6px solid transparent;
    border-left: 6px solid transparent;
    content: '';
    position: absolute;
    bottom: -6px;
    margin-left: -7px;
    left: 50%;
}

.map >>> .ol-tooltip-static:before {
    border-top-color: #000000;
}

.scale {
    position: absolute;
    right: calc(var(--padding-screen) * 2 + var(--width-button-normal));
    bottom: var(--padding-screen);
    background: rgba(255, 255, 255, 0.8);
    font-size: var(--font-size-tiny);
    font-weight: var(--font-weight-bold);
    color: black;
    user-select: none;
    cursor: pointer;
    z-index: 1;
}

.scale >>> .scale-text {
    height: 20px;
    line-height: 20px;
    padding: 0 4px;
}

.scale >>> .scale-line-inner {
    height: 20px;
    line-height: 20px;
    border: 2px solid black;
    border-top: none;
    text-align: center;
    will-change: contents, width;
    transition: all 0.25s ease;
}
</style>
