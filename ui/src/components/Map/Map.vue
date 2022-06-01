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

        <ListPanel
            v-if="this.showList && this.layers.length > 0"
            ref="listPanel"
            :layer="this.layers[1]"
            :titleTemplate="this.settings.title"
            :shortDescriptionTemplate="this.settings.short_description"
            @hidePanel="this.toggleList"
            @on-fit="(feature) => this.$refs.map.fit(feature, { maxZoom: 19 })"
        />
        <PointInfoPanel
            v-if="!this.showPanoramaPanel"
            :layers="this.layers"
            :position="this.position"
            :showInfoPanel="!showDataPanel && showInfoPanel"
            :user="this.user"
            :searchQuery="this.searchQuery"
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

            <div class="toggle-buttons">
                <Button
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
                </Button>
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
const reverseGeocodingEndpoint = 'https://geodata.nationaalgeoregister.nl/locatieserver/revgeo'

import OpenLayersRenderer from './renderers/OpenLayers/OpenLayers'

import Button from '../Button'
import ListPanel from '../ListPanel'
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
        settings: {
            type: Object,
            default: () => {
                return {}
            },
        },
        isEmbed: {
            type: Boolean,
            default: () => false,
        },
    },
    components: {
        Button,
        SearchPanel,
        LayersPanel,
        DataPanel,
        PointInfoPanel,
        ListPanel,
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
            showList: false,
            searchQuery: '',
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
                    this.searchQuery = `(${Math.round(position.marker[0] * 100) / 100},${
                        Math.round(position.marker[1] * 100) / 100
                    })`

                    return
                }

                const object = data.response.docs[0]
                this.searchQuery = object.weergavenaam
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
        toggleList() {
            this.showList = !this.showList
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

<style>
:root {
    --color-primary: #424bff;

    --color-text-grey: rgba(0, 0, 0, 0.55);

    --color-grey-20: #eaeaea; /* divider (list items, files) */
    --color-grey-30: #dddddd; /* divider (sections, header) */
    --color-grey-40: #f5f5f5;
    --color-grey-50: #eaeaea;
    --color-grey-60: #dadada;
    --color-grey-80: #949494;

    --color-icon-grey: rgba(0, 0, 0, 0.42);

    --color-tooltip-dark: #222222;

    --color-alert: #eb0000;

    --color-hover: rgba(0, 0, 0, 0.03);
    --color-active: rgba(0, 0, 0, 0.06);

    --font-size-tiny: 12px;
    --font-size-small: 14px;
    --font-size-normal: 16px;
    --font-size-large: 18px;

    --font-weight-normal: 300;
    --font-weight-bold: 500;

    --radius-small: 4px;
    --radius-normal: 8px;

    --shadow-normal: 0 0 1px rgba(0, 0, 0, 0.2), 0 0 8px rgba(0, 0, 0, 0.15);

    --padding-screen: 8px;

    --width-detail: 100vw;
    --width-button-small: 24px;
    --width-button-normal: 32px;
    --width-button-large: 40px;
}

@media (min-width: 576px) {
    :root {
        --width-detail: 300px;
        --padding-screen: 16px;
    }
}

@media (min-width: 768px) {
    :root {
        --width-detail: 350px;
    }
}

@media (min-width: 1200px) {
    :root {
        --width-detail: 400px;
        --padding-screen: 20px;
    }
}

@import url('https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,500;1,300;1,500&display=swap');

html {
    font-family: 'Roboto', sans-serif;
    font-size: var(--font-size-normal);
    font-weight: var(--font-weight-normal);
    line-height: 1.5;
}

*,
*:after,
*:before {
    box-sizing: border-box;
}

/* Remove outline from all focused elements */
*:focus {
    outline: none;
    outline-offset: -2px;
}

/* Remove highlight color on Android */
* {
    -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
}

html.keyboard-user *:focus {
    outline: 2px solid var(--color-primary);
}

input,
button {
    margin: 0;
    padding: 0;
    border: none;
    color: inherit;
    background: transparent;
    font: inherit;
    letter-spacing: inherit;
    text-align: left;
}

input::placeholder {
    color: var(--color-text-grey);
}

button:not([disabled]) {
    cursor: pointer;
}

ul {
    margin: 0;
    padding: 0;
    list-style-type: none;
}

svg {
    flex-shrink: 0;
}

.iconbutton {
    color: black;
    flex-shrink: 0;
    display: flex;
    align-items: center;
    justify-content: center;
    transition: border-radius 0.1s;
}

.iconbutton[disabled] {
    color: var(--color-grey-60);
}

.iconbutton.isActive {
    color: var(--color-primary);
}

.iconbutton:not([disabled]):hover {
    background: var(--color-grey-40);
}

.iconbutton:not([disabled]):active {
    background: var(--color-grey-50);
}

.iconbutton.__normal {
    width: 40px;
    height: 40px;
}

.iconbutton.__outline {
    border-radius: var(--radius-normal);
    border: 2px solid var(--color-grey-60);
}

.button:before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
}

.button {
    position: relative;
    display: flex;
    align-items: center;
    justify-content: center;
    height: 40px;
    padding: 0 20px;
    border-radius: var(--radius-normal);
    line-height: 1;
    font-size: var(--font-size-normal);
    font-weight: var(--font-weight-bold);
    text-decoration: none;
    overflow: hidden;
}

.button.__primary {
    background: var(--color-primary);
    color: white;
}
.button.__secondary {
    background: white;
    border: 2px solid var(--color-primary);
    color: var(--color-primary);
}
.button.__tertiary {
    background: white;
    border: 2px solid var(--color-grey-60);
    color: black;
}
.button.__alert {
    background: white;
    border: 2px solid var(--color-alert);
    color: var(--color-alert);
}

.button.__large {
    height: 56px;
    font-size: var(--font-size-large);
    border-width: 2px;
}

.button svg {
    margin-right: 6px;
}

.button:hover:before {
    background: var(--color-hover);
}
.button:active:before {
    background: var(--color-active);
}

@media (max-width: 575px) {
    .container {
        padding: 0 20px;
    }

    .section {
        padding: 32px 0;
    }
}

@media (min-width: 576px) {
    .container {
        padding: 0 32px;
    }

    .section {
        padding: 40px 0;
    }
}

.section + .section {
    padding-top: 0;
}

.flexer {
    display: flex;
    justify-content: center;
}

.flexer > *:not(:last-child) {
    margin-right: 12px;
}

.sidebar {
    flex-shrink: 0;
    position: relative;
    width: var(--width-detail);
    z-index: 1;
    box-shadow: var(--shadow-normal);
}

.sidebar h1 {
    height: 40px;
    margin: 0;
    font-size: var(--font-size-normal);
    font-weight: var(--font-weight-bold);

    display: flex;
    align-items: center;
    justify-content: center;
}

.sidebar h1 svg {
    margin-right: 6px;
}

.sidebar h2 {
    margin: 24px 0 8px;
    font-size: var(--font-size-normal);
    font-weight: var(--font-weight-bold);
}

.settings {
    margin: 0 calc(var(--padding-screen) * -1);
}

.setting {
    width: 100%;
    height: 41px;
    padding: 0 8px 0 16px;
    display: flex;
    align-items: center;
    font-weight: var(--font-weight-bold);
    border-top: 1px solid var(--color-grey-60);
}

.setting:last-child {
    border-bottom: 1px solid var(--color-grey-60);
}

.sidebar input[type='text'] {
    width: 100%;
    border: 1px solid var(--color-grey-80);
    border-radius: var(--radius-small);
    padding: 0 16px;
    height: 40px;
}
</style>
