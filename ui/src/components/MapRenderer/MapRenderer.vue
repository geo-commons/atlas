<template>
    <div class="map-container" :class="{ showInfoPanel: showInfoPanel, showDataPanel }">
        <div class="renderer-container">
            <OpenLayersRenderer
                ref="map"
                class="renderer"
                :position="this.position"
                :layers="this.layers"
                :tool="this.tool"
                :selectedArea="this.selectedArea"
                :highlightedFeatures="this.highlightedFeatures"
                :selectedFeatures="this.selectedFeatures"
                :padding="[0, 0, 0, 0]"
                :user="this.user"
                :features="this.features"
                :filters="this.filters"
                @position-changed="this.setPosition"
                @tool-used="this.toolUsed"
                @features-selected="this.featuresSelected"
            />
        </div>
        <ListPanel
            v-if="this.showList && this.layers.length > 0"
            ref="listPanel"
            :layer="this.layers[1]"
            :titleTemplate="this.settings.title"
            :shortDescriptionTemplate="this.settings.short_description"
            :filters="this.filters"
            @hidePanel="this.toggleList"
            @on-fit="(feature) => this.$refs.map.fit(feature, { maxZoom: 18 })"
        />
        <FilterPanel
            v-if="this.showFilters"
            ref="filterPanel"
            :layer="this.layers[1]"
            :facets="this.settings.facets"
            :filters="this.filters"
            :user="this.user"
            @hidePanel="this.toggleFilters"
            @update-filters="(value) => this.filters = value"
        />
        <PointInfoPanel
            v-if="!this.showPanoramaPanel && this.features.markerOnClick"
            :layers="this.layers"
            :position="this.position"
            :showPanel="!showDataPanel && showInfoPanel"
            :user="this.user"
            @set-position="this.setPosition"
        />
        <DetailPanel
            v-if="!this.showPanoramaPanel && !this.features.markerOnClick && this.features.detail"
            :showPanel="this.selectedFeatures.length > 0"
            :features="this.selectedFeatures"
            @features-selected="this.featuresSelected"
        />
        <DataPanel
            v-if="!this.isEmbed && !this.showPanoramaPanel"
            ref="dataPanel"
            :layers="this.layers"
            :position="this.position"
            :selectedArea="this.selectedArea"
            :showDataPanel="showDataPanel"
            :user="this.user"
            @set-position="this.setPosition"
            @on-fit="(layer) => this.$refs.map.fit(layer, { maxZoom: 18 })"
            @toggle-data-panel="this.toggleDataPanel"
        />

        <div class="ui-container">
            <SearchPanel
                v-if="this.features.searchbar"
                :position="this.position"
                @set-position="this.setPosition"
                @toggle-data-panel="this.toggleDataPanel"
            />

            <div class="toggle-buttons">
                <PrimaryButton
                    v-if="this.features.list && !this.showList"
                    size="large"
                    label="Lijst"
                    dropShadow
                    @click="this.toggleList"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        enable-background="new 0 0 24 24"
                        height="24px"
                        viewBox="0 0 24 24"
                        width="24px"
                        fill="#000000"
                    >
                        <rect fill="none" height="24" width="24" />
                        <path
                            d="M3,5v14h18V5H3z M7,7v2H5V7H7z M5,13v-2h2v2H5z M5,15h2v2H5V15z M19,17H9v-2h10V17z M19,13H9v-2h10V13z M19,9H9V7h10V9z"
                        />
                    </svg>
                </PrimaryButton>
                <PrimaryButton
                    v-if="this.features.filters && !this.showFilters"
                    size="large"
                    label="Verfijn"
                    dropShadow
                    @click="this.toggleFilters"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        height="24px"
                        viewBox="0 0 24 24"
                        width="24px"
                        fill="#000000"
                    >
                        <path d="M0 0h24v24H0V0z" fill="none" />
                        <path d="M10 18h4v-2h-4v2zM3 6v2h18V6H3zm3 7h12v-2H6v2z" />
                    </svg>
                </PrimaryButton>
            </div>

            <div class="top-right-panels">
                <ToolsPanel
                    :features="this.features"
                    :tool="this.tool"
                    @set-tool="this.setTool"
                    @set-selected-area="this.setSelectedArea"
                />
            </div>
            <div class="bottom-left-panels">
                <LayersPanel
                    v-if="this.features.layerlist || this.features.legend"
                    :layers="this.layers"
                    :position="this.position"
                    :user="this.user"
                    :isEmbed="this.features.legend && !this.features.layerlist"
                    @toggle-layer="this.toggleLayer"
                    @set-layer-opacity="this.setLayerOpacity"
                    @on-fit="(layer) => this.$refs.map.fit(layer)"
                />
            </div>
            <div class="bottom-right-panels">
                <GeoLocationButton v-if="this.features.gps" @set-position="this.setPosition" />
                <ZoomPanel
                    v-if="this.features.zoom"
                    :position="this.position"
                    @set-position="this.setPosition"
                />
            </div>
        </div>
    </div>
</template>

<script>
const reverseGeocodingEndpoint = 'https://api.pdok.nl/bzk/locatieserver/search/v3_1/reverse'

import GeoJSON from 'ol/format/GeoJSON'
import TileWMS from 'ol/source/TileWMS'
import View from 'ol/View'
import OpenLayersRenderer from './renderers/OpenLayers/OpenLayers'

import PrimaryButton from '../PrimaryButton'
import ListPanel from '../ListPanel'
import FilterPanel from '../FilterPanel'
import DataPanel from '../DataPanel'
import PointInfoPanel from '../PointInfoPanel'
import DetailPanel from '../DetailPanel'
import SearchPanel from '../SearchPanel'
import LayersPanel from '../LayersPanel'
import ToolsPanel from '../ToolsPanel'
import ZoomPanel from '../ZoomPanel'
import GeoLocationButton from '../GeoLocationButton'

export default {
    name: 'MapRenderer',
    props: {
        initialLayers: Array,
        initialPosition: Object,
        user: Object,
        features: {
            type: Object,
            default: () => {
                return {
                    scale: true,
                }
            },
        },
        settings: {
            type: Object,
            default: () => {
                return {
                    facets: []
                }
            },
        },
        isEmbed: {
            type: Boolean,
            default: () => false,
        },
    },
    components: {
        PrimaryButton,
        SearchPanel,
        LayersPanel,
        DataPanel,
        PointInfoPanel,
        DetailPanel,
        ListPanel,
        FilterPanel,
        OpenLayersRenderer,
        ToolsPanel,
        ZoomPanel,
        GeoLocationButton,
    },
    data() {
        return {
            layers: this.initialLayers,
            position: this.initialPosition,
            highlightedFeatures: [],
            selectedFeatures: [],
            tool: '',
            selectedArea: null,
            showDataPanel: false,
            showPanoramaPanel: false,
            showList: false,
            showFilters: false,
            filters: {}
        }
    },
    methods: {
        async setPosition(position) {
            this.position = position
            this.$emit('position-changed', position)

            if (!position.marker) {
                return
            }

            this.reverseGeocode(position)
            this.getFeatureInfo(position)
        },
        async reverseGeocode(position) {
            try {
                const result = await fetch(
                    `${reverseGeocodingEndpoint}?X=${position.marker[0]}&Y=${position.marker[1]}&rows=1&distance=20`
                )
                const data = await result.json()

                if (!data.response.docs || data.response.docs.length === 0) {
                    this.$store.commit(
                        'setSearchQuery',
                        `(${Math.round(position.marker[0] * 100) / 100},${
                            Math.round(position.marker[1] * 100) / 100
                        })`
                    )
                    return
                }

                const object = data.response.docs[0]
                this.$store.commit('setSearchQuery', object.weergavenaam)
            } catch (e) {
                console.error(e)
            }
        },
        async getFeatureInfo(position) {
            this.highlightedFeatures = []

            const visibleLayers = this.layers.filter((layer) => layer.is_selectable && !layer.is_base && layer.is_visible)
            visibleLayers.forEach(async (layer) => {
                const wmsSource = new TileWMS({
                    url: layer.url,
                    servertype: layer.server_type,
                    params: {
                        LAYERS: layer.name,
                        TILED: true,
                    },
                })

                const view = new View({
                    center: this.position.center,
                    zoom: this.position.zoom,
                })

                const url = wmsSource.getFeatureInfoUrl(
                    position.marker,
                    view.getResolution(),
                    'EPSG:28992',
                    {
                        info_format: 'application/json',
                        feature_count: 20,
                    }
                )

                try {
                    const result = await fetch(url)
                    const data = await result.json()
                    this.highlightedFeatures = [
                        ...this.highlightedFeatures,
                        ...data.features.map(feature => new GeoJSON().readFeature(feature))
                    ]
                } catch (e) {
                    console.error(e)
                }
            })
        },
        toggleDataPanel() {
            this.showDataPanel = !this.showDataPanel

            if (!this.showDataPanel) {
                this.selectedArea = null
            }
        },
        toggleList() {
            this.showList = !this.showList
        },
        toggleFilters() {
            this.showFilters = !this.showFilters
        },
        setTool(tool) {
            this.tool = tool
        },
        toolUsed(result) {
            if (result && result.sketch) {
                this.selectedArea = result.sketch.getGeometry()
            }

            switch (result.tool) {
                case 'SELECT_AREA':
                    this.showDataPanel = true
                    break
            }
        },
        featuresSelected(selectedFeatures) {
            this.selectedFeatures = selectedFeatures
        },
        setSelectedArea(selectedArea) {
            this.selectedArea = selectedArea
        },
        toggleLayer([layerId, isVisible]) {
            this.layers = this.layers.map((layer) =>
                layer.id == layerId ? { ...layer, is_visible: isVisible } : layer
            )
        },
        setLayerOpacity([layerId, opacity]) {
            this.layers = this.layers.map((layer) =>
                layer.id == layerId ? { ...layer, opacity: opacity } : layer
            )
        },
    },
    watch: {
        initialPosition(value) {
            this.position = value
        },
        initialLayers(value) {
            this.layers = value
        },
    },
    computed: {
        showInfoPanel() {
            return this.position.marker ? true : false
        },
    },
}
</script>

<style scoped>
.map-container {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
}

.renderer-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-flow: column;
}

@media (max-width: 575px) {
    .ui-container {
        order: -1;
    }
}

.ui-container {
    z-index: 1;
    flex-grow: 1;
    height: 100%;
    position: relative;
    pointer-events: none;
}

.ui-container > * {
    pointer-events: auto;
}

.map {
    flex: 1 1 auto;
    height: 0; /* fixes incorrect display of .ol-viewport on Safari 13.1 */
}

.top-right-panels {
    z-index: 1;
    position: absolute;
    top: var(--padding-screen);
    right: var(--padding-screen);
}

.bottom-left-panels {
    z-index: 1;
    position: absolute;
    bottom: var(--padding-screen);
    left: var(--padding-screen);
}

.bottom-right-panels {
    z-index: 1;
    position: absolute;
    bottom: var(--padding-screen);
    right: var(--padding-screen);
    display: flex;
    flex-direction: column;
}

.bottom-right-panels > *:not(:last-child) {
    margin-bottom: 12px;
}

.toggle-buttons {
    position: absolute;
    top: var(--padding-screen);
    left: var(--padding-screen);
    display: flex;
}

.toggle-buttons > *:not(:last-child) {
    margin-right: 8px;
}
</style>
