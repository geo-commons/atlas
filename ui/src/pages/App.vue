<template>
    <div
        class="container"
        :style="computedStyle"
        :class="{ showInfoPanel: showInfoPanel, showDataPanel }"
    >
        <SearchPanel
            :position="this.position"
            @set-position="this.setPosition"
            @toggle-data-panel="this.toggleDataPanel"
        />
        <PointInfoPanel
            v-if="!this.isEmbed"
            :layers="this.layers"
            :position="this.position"
            :showInfoPanel="!showDataPanel && showInfoPanel"
            @set-position="this.setPosition"
        />
        <DataPanel
            v-if="!this.isEmbed"
            ref="dataPanel"
            :layers="this.layers"
            :position="this.position"
            :selectedArea="this.selectedArea"
            :showDataPanel="showDataPanel"
            @set-position="this.setPosition"
            @toggle-data-panel="this.toggleDataPanel"
        />

        <div class="map">
            <Map
                ref="map"
                :position="this.position"
                :layers="this.layers"
                :extent="this.config.extent"
                :tool="this.tool"
                :selectedArea="this.selectedArea"
                :padding="this.mapPadding"
                @set-position="this.setPosition"
                @tool-used="this.toolUsed"
            />
            <div class="top-right-panels">
                <Tools
                    v-if="!this.isEmbed"
                    :tool="this.tool"
                    @set-tool="this.setTool"
                    @set-selected-area="this.setSelectedArea"
                />
                <MorePanel v-if="!this.isEmbed" :user="this.user" @toggle-modal="toggleModal" />
            </div>
            <div class="bottom-left-panels">
                <LayersPanel
                    v-if="!this.isEmbed"
                    :layers="this.layers"
                    :position="this.position"
                    @toggle-layer="this.toggleLayer"
                    @set-layer-opacity="this.setLayerOpacity"
                    @on-fit="(layer) => this.$refs.map.fit(layer)"
                />
            </div>
            <div class="bottom-right-panels">
                <div class="bottom-right-wrapper">
                    <div
                        v-if="!this.isEmbed"
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
                        <transition name="fade">
                            <PanoramaPanel
                                :position="this.position"
                                :isOpen="showPanoramaPanel"
                                @toggle="togglePanoramaPanel"
                            />
                        </transition>
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
                </div>
                <div class="bottom-right-wrapper">
                    <GeoLocationButton @set-position="this.setPosition" />
                </div>
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
import { getArea, getLength } from 'ol/sphere'
import { isMobile } from '../utils/helpers'
import Alert from '../components/Alert'
import BaseLayersPanel from '../components/BaseLayersPanel'
import DataPanel from '../components/DataPanel'
import EmbedModal from '../components/EmbedModal'
import LayersPanel from '../components/LayersPanel'
import Map from '../components/Map'
import Tools from '../components/Tools'
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
        Map,
        Tools,
        MorePanel,
        PanoramaPanel,
        PointInfoPanel,
        SearchPanel,
        ZoomPanel,
        GeoLocationButton,
    },
    computed: mapState({
        isEmbed: (state) => state.isEmbed,
        config: (state) => state.config,
        alert: (state) => state.alert,
        position: (state) => state.position,
        layers: (state) => state.layers,
        tool: (state) => state.tool,
        user: (state) => state.user,
        selectedArea: (state) => state.selectedArea,
    }),
    created() {
        window.addEventListener('resize', this.onResizeWindow)
        this.setViewportHeight()
    },
    destroyed() {
        window.removeEventListener('resize', this.onResizeWindow)
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
            let measureResult

            switch (result.tool) {
                case 'MEASURE_AREA':
                    measureResult = getArea(result.sketch.getGeometry())
                    alert(`${Math.round(measureResult * 100) / 100} m2`)
                    break
                case 'MEASURE_LINE':
                    measureResult = getLength(result.sketch.getGeometry())
                    alert(`${Math.round(measureResult * 100) / 100} m`)
                    break
                case 'SELECT_AREA':
                    this.$store.commit('setSelectedArea', result.sketch.getGeometry())
                    this.showDataPanel = true
                    break
            }

            setTimeout(() => {
                this.$store.commit('setTool', '')
            }, 500)
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
        async searchAddress() {
            const position = this.position

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
    },
    watch: {
        position(value) {
            this.showInfoPanel = Boolean(value.marker)
            this.pushHistoryState()
            this.searchAddress()
        },
        layers(value) {
            this.pushHistoryState()
        },
    },
    data() {
        return {
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

    --font-size-tiny: 14px;
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
    font-size: var(--font-size-tiny);
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
    width: 100%;
    height: 100%;
    display: flex;
}

.map {
    position: relative;
    flex-grow: 1;
}

.bottom-left-panels {
    position: absolute;
    bottom: var(--padding-screen);
    left: var(--padding-screen);
}

@media (max-width: 575px) {
    .showInfoPanel .bottom-left-panels,
    .showDataPanel .bottom-left-panels,
    .showInfoPanel .bottom-right-panels,
    .showDataPanel .bottom-right-panels {
        bottom: calc((40 * var(--vh)) + var(--padding-screen));
    }
}

@media (min-width: 576px) {
    .showInfoPanel .bottom-left-panels {
        left: calc(var(--padding-screen) + var(--width-detail));
    }
    .showDataPanel .bottom-left-panels {
        left: calc(var(--padding-screen) + 50%);
    }
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

.bottom-right-wrapper {
    position: relative;
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
