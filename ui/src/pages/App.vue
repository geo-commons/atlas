<template>
    <div
        class="container"
        :style="computedStyle"
        :class="{ showInfoPanel: showInfoPanel, showDataPanel }"
    >
        <div class="map-container">
            <PanoramaPanel
                class="panorama-panel"
                :position="this.position"
                :isOpen="showPanoramaPanel"
                @toggle="togglePanoramaPanel"
            />
            <OpenLayersRenderer
                v-if="this.readyToRenderMap"
                ref="map"
                class="map"
                :position="this.position"
                :layers="this.layers"
                :tool="this.tool"
                :selectedArea="this.selectedArea"
                :padding="this.mapPadding"
                :user="this.user"
                @set-position="this.setPosition"
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
                v-if="!this.showPanoramaPanel"
                :position="this.position"
                @set-position="this.setPosition"
                @toggle-data-panel="this.toggleDataPanel"
            />
            <div class="top-right-panels">
                <ToolsPanel
                    v-if="!this.isEmbed && !this.showPanoramaPanel"
                    :tool="this.tool"
                    @set-tool="this.setTool"
                    @set-selected-area="this.setSelectedArea"
                />
                <MorePanel
                    v-if="!this.isEmbed && !this.showPanoramaPanel"
                    :user="this.user"
                    :showDisclaimer="this.config.show_disclaimer"
                    @toggle-modal="toggleModal"
                />
            </div>
            <div class="bottom-left-panels">
                <LayersPanel
                    v-if="!this.showPanoramaPanel"
                    :isEmbed="this.isEmbed"
                    :layers="this.layers"
                    :position="this.position"
                    :user="this.user"
                    @toggle-layer="this.toggleLayer"
                    @set-layer-opacity="this.setLayerOpacity"
                    @on-fit="(layer) => this.$refs.map.fit(layer)"
                />
            </div>
            <div class="bottom-right-panels">
                <div
                    v-if="!this.isEmbed && !this.showPanoramaPanel"
                    class="bottom-right-buttons"
                    :class="{
                        isOpen: showBaseLayersPanel,
                        showTogglePanorama: position.marker || showPanoramaPanel,
                    }"
                >
                    <button
                        class="iconbutton"
                        @click="togglePanoramaPanel"
                        v-tippy="{ placement: 'left' }"
                        content="Panorama"
                        aria-label="Toon panorama"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            height="24"
                            viewBox="0 0 24 24"
                            width="24"
                        >
                            <path d="M0 0h24v24H0z" fill="none" />
                            <path
                                d="M12 7C6.48 7 2 9.24 2 12c0 2.24 2.94 4.13 7 4.77V20l4-4-4-4v2.73c-3.15-.56-5-1.9-5-2.73 0-1.06 3.04-3 8-3s8 1.94 8 3c0 .73-1.46 1.89-4 2.53v2.05c3.53-.77 6-2.53 6-4.58 0-2.76-4.48-5-10-5z"
                            />
                        </svg>
                    </button>
                    <button
                        class="iconbutton"
                        @click="toggleBaseLayersPanel"
                        v-tippy="{ placement: 'left' }"
                        content="Basislagen"
                        aria-label="Toon basislagen"
                        :aria-expanded="showBaseLayersPanel.toString()"
                        aria-controls="baseLayers"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            height="24"
                            viewBox="0 0 24 24"
                            width="24"
                        >
                            <path d="M0 0h24v24H0V0z" fill="none" />
                            <path
                                d="M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1 5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5zM10 5.47l4 1.4v11.66l-4-1.4V5.47zm-5 .99l3-1.01v11.7l-3 1.16V6.46zm14 11.08l-3 1.01V6.86l3-1.16v11.84z"
                            />
                        </svg>
                    </button>
                    <transition name="fade">
                        <BaseLayersPanel
                            v-if="showBaseLayersPanel"
                            :layers="this.layers"
                            @toggle-layer="this.toggleLayer"
                        />
                    </transition>
                </div>
                <GeoLocationButton @set-position="this.setPosition" />
                <ZoomPanel :position="this.position" @set-position="this.setPosition" />
            </div>
        </div>

        <transition name="fade">
            <EmbedModal
                v-if="modal === 'embed'"
                :layers="layers"
                :position="position"
                @toggle-modal="toggleModal"
            />
        </transition>
        <Alert :alert="this.alert" />
    </div>
</template>

<script>
import { mapState } from 'vuex'
import { isMobile } from '../utils/helpers'
import Alert from '../components/Alert'
import BaseLayersPanel from '../components/BaseLayersPanel'
import DataPanel from '../components/DataPanel'
import EmbedModal from '../components/EmbedModal'
import LayersPanel from '../components/LayersPanel'
import OpenLayersRenderer from '../components/Map/renderers/OpenLayers'
import ToolsPanel from '../components/ToolsPanel'
import MorePanel from '../components/MorePanel'
import PanoramaPanel from '../components/PanoramaPanel'
import PointInfoPanel from '../components/PointInfoPanel'
import SearchPanel from '../components/SearchPanel'
import ZoomPanel from '../components/ZoomPanel'
import GeoLocationButton from '../components/GeoLocationButton'

const reverseGeocodingEndpoint = 'https://geodata.nationaalgeoregister.nl/locatieserver/revgeo'

export default {
    name: 'App',
    components: {
        Alert,
        BaseLayersPanel,
        DataPanel,
        EmbedModal,
        LayersPanel,
        OpenLayersRenderer,
        ToolsPanel,
        MorePanel,
        PanoramaPanel,
        PointInfoPanel,
        SearchPanel,
        ZoomPanel,
        GeoLocationButton,
    },
    computed: mapState({
        isEmbed: (state) => state.isEmbed,
        alert: (state) => state.alert,
        position: (state) => state.position,
        layers: (state) => state.layers,
        tool: (state) => state.tool,
        user: (state) => state.user,
        config: (state) => state.config,
        selectedArea: (state) => state.selectedArea,
    }),
    created() {
        window.addEventListener('resize', this.onResizeWindow)
        this.setViewportHeight()

        if (!this.user) {
            this.readyToRenderMap = true
            return
        }

        this.fetchAccessToken()

        this.fetchInterval = setInterval(() => {
            this.fetchAccessToken()
        }, 1000 * 60 * 10) // every ten minutes
    },
    destroyed() {
        window.removeEventListener('resize', this.onResizeWindow)
        clearInterval(this.fetchInterval)
    },
    methods: {
        onResizeWindow() {
            this.setViewportHeight()
        },
        setViewportHeight() {
            this.computedStyle['--vh'] = window.innerHeight / 100 + 'px'
        },
        async setPosition(position) {
            this.$store.commit('setPosition', position)

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
        toggleLayer(values) {
            this.$store.commit('toggleLayer', values)
        },
        setLayerOpacity(values) {
            this.$store.commit('setLayerOpacity', values)
        },
        setTool(tool) {
            this.$store.commit('setTool', tool)
        },
        setSelectedArea(selectedArea) {
            this.$store.commit('setSelectedArea', selectedArea)
        },
        toolUsed(result) {
            if (result && result.sketch) {
                this.$store.commit('setSelectedArea', result.sketch.getGeometry())
            }

            switch (result.tool) {
                case 'SELECT_AREA':
                    this.showDataPanel = true
                    break
            }
        },
        toggleInfoPanel() {
            this.showInfoPanel = !this.showInfoPanel
        },
        togglePanoramaPanel() {
            this.showBaseLayersPanel = false
            this.showPanoramaPanel = !this.showPanoramaPanel
        },
        toggleBaseLayersPanel() {
            this.showPanoramaPanel = false
            this.showBaseLayersPanel = !this.showBaseLayersPanel
        },
        pushHistoryState() {
            const basePath = /(.*?)(@|$)/.exec(window.location.pathname)

            const x = encodeURIComponent(this.position.center[0].toFixed(2))
            const y = encodeURIComponent(this.position.center[1].toFixed(2))
            const zoom = encodeURIComponent(this.position.zoom)
            const layers = this.layers
                .filter((l) => l.is_visible && !l.is_base)
                .map((l) => l.id)
                .join(',')

            window.history.replaceState(
                {},
                '',
                `${basePath[1]}@${x},${y},${zoom}z/layers=${layers}`
            )
        },
        toggleModal(modal) {
            this.modal = modal
        },
        toggleDataPanel() {
            this.showDataPanel = !this.showDataPanel
            if (!this.showDataPanel) {
                this.$store.commit('setSelectedArea', null)
            }

            if (!isMobile() && this.showDataPanel) {
                this.$set(this.mapPadding, 3, window.innerWidth * 0.5)
            } else {
                this.$set(this.mapPadding, 3, 0)
            }
        },
        async fetchAccessToken() {
            const response = await fetch('/atlas/api/v1/token')
            if (!response.ok) {
                this.readyToRenderMap = true
                return false
            }

            const data = await response.json()
            this.$store.commit('setUser', {
                ...this.user,
                token: data.token,
            })

            this.readyToRenderMap = true
        },
    },
    watch: {
        position(value) {
            this.showInfoPanel = Boolean(value.marker)
            this.pushHistoryState()
        },
        layers(value) {
            this.pushHistoryState()
        },
    },
    data() {
        return {
            readyToRenderMap: false,
            showInfoPanel: Boolean(this.position && this.position.marker),
            showPanoramaPanel: false,
            showBaseLayersPanel: false,
            showDataPanel: false,
            computedStyle: { '--color-primary': '#0066FF' },
            modal: '',
            mapPadding: [0, 0, 0, 0],
        }
    },
}
</script>

<style>
:root {
    --color-text-grey: rgba(0, 0, 0, 0.55);

    --color-grey-40: #f5f5f5;
    --color-grey-50: #eaeaea;
    --color-grey-60: #dadada;

    --color-icon-grey: rgba(0, 0, 0, 0.42);

    --color-tooltip-dark: #222222;

    --color-alert: #eb0000;

    --font-size-tiny: 12px;
    --font-size-small: 14px;
    --font-size-normal: 16px;

    --font-weight-normal: 400;
    --font-weight-bold: 700;

    --radius-small: 3px;
    --radius-normal: 6px;

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

@import url('https://fonts.googleapis.com/css2?family=PT+Sans:wght@400;700&display=swap');

html {
    font-family: 'PT Sans', sans-serif;
    letter-spacing: -0.005em;
    font-size: var(--font-size-normal);
    font-weight: var(--font-weight-normal);
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

.menu {
    padding: 6px 0;
    background: white;
    border-radius: var(--radius-small);
    border-top-right-radius: 0;
    box-shadow: var(--shadow-normal);
}

.list a,
.list button {
    display: block;
    width: 100%;
    color: black;
    text-decoration: none;
    padding: 4px 12px;
    font-size: var(--font-size-small);
}

.list a:hover,
.list button:hover {
    background: var(--color-grey-40);
}

.list a:active,
.list button:active {
    background: var(--color-grey-50);
}

.counter {
    flex-shrink: 0;
    height: 18px;
    min-width: 18px;
    border-radius: 9px;
    border: 2px solid var(--color-primary);
    padding: 0 3px;
    background: white;
    color: var(--color-primary);
    font-size: 11px;
    font-weight: var(--font-weight-bold);
    line-height: 14px;
    text-align: center;
    white-space: nowrap;
    user-select: none;
}

.fade-enter-active,
.fade-leave-active {
    transition: opacity 0.1s;
}
.fade-enter,
.fade-leave-to {
    opacity: 0;
}

.tippy-tooltip {
    padding: 0;
    border-radius: var(--radius-normal);
    font-family: inherit;
    font-size: var(--font-size-small);
    font-weight: var(--font-weight-bold);
    letter-spacing: 0em;
}

.tippy-tooltip .tippy-content {
    padding: 3px 7px 4px;
}

.tippy-tooltip.dark-theme .tippy-backdrop {
    background-color: var(--color-tooltip-dark);
}

.tippy-tooltip.primary-theme .tippy-backdrop {
    /* TODO: var(--color-primary) doesn't work */
    background-color: #0066ff;
}

.tippy-tooltip.popover-theme {
    background-color: white;
    font-size: var(--font-size-small);
    font-weight: var(--font-weight-normal);
    color: #000000;
    letter-spacing: inherit;
    box-shadow: var(--shadow-normal);
}

.tippy-tooltip.popover-theme[x-placement^='left'] .tippy-arrow {
    border-left-color: white;
}

.tippy-tooltip.popover-theme[x-placement^='right'] .tippy-arrow {
    border-right-color: white;
}

.tippy-tooltip.popover-theme .tippy-content {
    padding: 0;
    overflow: auto;
}
</style>

<style scoped>
.container {
    position: relative;
    width: 100%;
    height: 100%;
    display: flex;
}

@media (max-width: 575px) {
    .container {
        flex-direction: column;
    }

    .ui-container {
        order: -1;
    }
}

.ui-container {
    flex-grow: 1;
    height: 100%;
    position: relative;
    pointer-events: none;
}

.ui-container > * {
    pointer-events: auto;
}

.map-container {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    display: flex;
    flex-flow: column;
}

.panorama-panel {
    flex: 0 1 auto;
}

.map {
    flex: 1 1 auto;
    height: 0; /* fixes incorrect display of .ol-viewport on Safari 13.1 */
}

.bottom-left-panels {
    position: absolute;
    bottom: var(--padding-screen);
    left: var(--padding-screen);
}

.top-right-panels {
    position: absolute;
    top: calc((var(--padding-screen) * 2) + var(--width-button-large));
    right: var(--padding-screen);
    display: flex;
}

@media (min-width: 576px) {
    .top-right-panels {
        top: var(--padding-screen);
    }
}

.bottom-right-panels {
    position: absolute;
    bottom: var(--padding-screen);
    right: var(--padding-screen);
    display: flex;
    flex-direction: column;
}

.bottom-right-panels > *:not(:last-child) {
    margin-bottom: 12px;
}

.bottom-right-buttons {
    display: flex;
    flex-direction: column;
    justify-content: flex-end;
    background: white;
    border-radius: var(--radius-normal);
    overflow: hidden;
    box-shadow: var(--shadow-normal);
    height: var(--width-button-normal);
    transition: height 0.1s ease, border-radius 0.1s;
    overflow: hidden;
}

.bottom-right-buttons.isOpen {
    border-top-left-radius: 0;
    border-top-right-radius: 0;
}

.bottom-right-buttons.showTogglePanorama {
    height: calc(var(--width-button-normal) * 2 + 1px);
}

.bottom-right-buttons .iconbutton {
    width: var(--width-button-normal);
    height: var(--width-button-normal);
}

.bottom-right-buttons .iconbutton:first-child {
    box-sizing: content-box;
    border-bottom: 1px solid var(--color-grey-50);
}
</style>
