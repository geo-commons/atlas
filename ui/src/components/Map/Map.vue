<template>
    <div class="map-container">
        <OpenLayersRenderer
            ref="map"
            class="map"
            :position="this.position"
            :layers="this.layers"
            :tool="this.tool"
            :selectedArea="this.selectedArea"
            :padding="this.padding"
            :user="this.user"
            :features="this.features"
        />
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
                v-if="this.features.layerlist"
                :layers="this.layers"
                :position="this.position"
                :user="this.user"
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
</template>

<script>
import OpenLayersRenderer from './renderers/OpenLayers/OpenLayers'

import SearchPanel from '../SearchPanel'
import LayersPanel from '../LayersPanel'
import ToolsPanel from '../ToolsPanel'
import ZoomPanel from '../ZoomPanel'
import GeoLocationButton from '../GeoLocationButton'

export default {
    name: 'Map',
    props: {
        position: Object,
        layers: Array,
        tool: String,
        selectedArea: Object,
        user: Object,
        features: {
            type: Object,
            default: () => {
                return {
                    scale: true,
                }
            },
        },
        padding: { type: Array, default: () => [0, 0, 0, 0] },
    },
    components: {
        SearchPanel,
        LayersPanel,
        OpenLayersRenderer,
        ToolsPanel,
        ZoomPanel,
        GeoLocationButton,
    },
    methods: {
        setPosition(position) {
            return
        },
        toggleDataPanel() {
            return
        },
        setTool() {
            return
        },
        setSelectedArea() {
            return
        },
        setLayerOpacity() {
            return
        },
        toggleLayer() {
            return
        },
    },
}
</script>

<style scoped>
.container {
    width: 100%;
    height: 100%;
    display: flex;
}

.map-container {
    flex-grow: 1;
    position: relative;
    display: flex;
    flex-flow: column;
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
