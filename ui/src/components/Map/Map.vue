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
                :padding="[0, 0, 0, 0]"
                :user="this.user"
                :features="this.features"
                @position-changed="this.setPosition"
                @tool-used="this.toolUsed"
            />
        </div>

        <PointInfoPanel
            v-if="!this.showPanoramaPanel"
            :layers="this.layers"
            :position="this.position"
            :showInfoPanel="!showDataPanel && showInfoPanel"
            :user="this.user"
            @set-position="this.setPosition"
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
            @on-fit="(layer) => this.$refs.map.fit(layer, { maxZoom: 19 })"
            @toggle-data-panel="this.toggleDataPanel"
        />

        <div class="ui-container">
            <SearchPanel
                v-if="this.features.searchbar"
                :position="this.position"
                @set-position="this.setPosition"
                @toggle-data-panel="this.toggleDataPanel"
            />
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
const reverseGeocodingEndpoint = 'https://geodata.nationaalgeoregister.nl/locatieserver/revgeo'

import OpenLayersRenderer from './renderers/OpenLayers/OpenLayers'

import DataPanel from '../DataPanel'
import PointInfoPanel from '../PointInfoPanel'
import SearchPanel from '../SearchPanel'
import LayersPanel from '../LayersPanel'
import ToolsPanel from '../ToolsPanel'
import ZoomPanel from '../ZoomPanel'
import GeoLocationButton from '../GeoLocationButton'

export default {
    name: 'Map',
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
        isEmbed: {
            type: Boolean,
            default: () => false,
        },
    },
    components: {
        SearchPanel,
        LayersPanel,
        DataPanel,
        PointInfoPanel,
        OpenLayersRenderer,
        ToolsPanel,
        ZoomPanel,
        GeoLocationButton,
    },
    data() {
        return {
            layers: this.initialLayers,
            position: this.initialPosition,
            tool: '',
            selectedArea: null,
            showDataPanel: false,
            showPanoramaPanel: false,
        }
    },
    methods: {
        async setPosition(position) {
            this.position = position

            if (!position.marker) {
                return
            }

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
        toggleDataPanel() {
            this.showDataPanel = !this.showDataPanel

            if (!this.showDataPanel) {
                this.selectedArea = null
            }
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
</style>
