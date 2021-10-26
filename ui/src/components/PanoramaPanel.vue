<template>
    <vue-resizable
        :active="this.isFullscreen ? null : ['b']"
        width="auto"
        :minHeight="windowHeight / 6"
        :maxHeight="(windowHeight / 6) * 5"
        :height="this.isFullscreen ? windowHeight : windowHeight / 2"
        :fitParent="true"
        :style="{ display: isOpen ? 'block' : 'none' }"
        dragSelector="undefined"
        @resize:move="this.onResize"
    >
        <div class="buttons">
            <button
                class="iconbutton"
                :aria-label="isFullscreen ? 'Verkleinen' : 'Vergroten'"
                @click="toggleSize"
            >
                <svg
                    v-if="!isFullscreen"
                    xmlns="http://www.w3.org/2000/svg"
                    height="24"
                    viewBox="0 0 24 24"
                    width="24"
                >
                    <path d="M0 0h24v24H0z" fill="none" />
                    <path
                        d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"
                    />
                </svg>
                <svg
                    v-if="isFullscreen"
                    xmlns="http://www.w3.org/2000/svg"
                    height="24"
                    viewBox="0 0 24 24"
                    width="24"
                >
                    <path d="M0 0h24v24H0z" fill="none" />
                    <path
                        d="M5 16h3v3h2v-5H5v2zm3-8H5v2h5V5H8v3zm6 11h2v-3h3v-2h-5v5zm2-11V5h-2v5h5V8h-3z"
                    />
                </svg>
            </button>
            <button class="iconbutton" aria-label="Sluiten" @click="toggle">
                <svg
                    width="14px"
                    height="14px"
                    viewBox="0 0 14 14"
                    version="1.1"
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink"
                >
                    <title>Path</title>
                    <g
                        id="Wireframes"
                        stroke="none"
                        stroke-width="1"
                        fill="none"
                        fill-rule="evenodd"
                    >
                        <g
                            id="streetview"
                            transform="translate(-985.000000, -413.000000)"
                            fill="#000000"
                            fill-rule="nonzero"
                        >
                            <g id="Group-5" transform="translate(976.000000, 404.000000)">
                                <polygon
                                    id="Path"
                                    points="23 10.41 21.59 9 16 14.59 10.41 9 9 10.41 14.59 16 9 21.59 10.41 23 16 17.41 21.59 23 23 21.59 17.41 16"
                                ></polygon>
                            </g>
                        </g>
                    </g>
                </svg>
            </button>
        </div>
        <div class="viewer" ref="viewer">
            <div v-if="!viewer" class="message">
                Er is geen panoramaweergave beschikbaar. Controleer de configuratie van Google Maps
                of StreetSmart.
            </div>
        </div>
    </vue-resizable>
</template>

<script>
import VueResizable from 'vue-resizable'
import { GooglePanorama, StreetSmartPanorama } from '../utils/panorama'

export default {
    name: 'PanoramaPanel',
    components: {
        VueResizable,
    },
    created() {
        window.addEventListener('resize', this.onResizeWindow)
        this.setViewportWidth()
        this.setViewportHeight()
    },
    destroyed() {
        window.removeEventListener('resize', this.onResizeWindow)
    },
    data() {
        return {
            isFullscreen: false,
            viewer: null,
            windowWidth: 200,
            windowHeight: 200,
        }
    },
    methods: {
        toggle() {
            this.$emit('toggle')
        },
        async toggleSize() {
            this.isFullscreen = !this.isFullscreen

            await this.$nextTick()

            this.onResize()
        },
        onResize() {
            this.viewer.resize()
        },
        onResizeWindow() {
            this.setViewportWidth()
            this.setViewportHeight()
        },
        setViewportWidth() {
            this.windowWidth = window.innerWidth
        },
        setViewportHeight() {
            this.windowHeight = window.innerHeight
        },
    },
    watch: {
        isOpen(value) {
            // Make sure the div of the viewer is visible in the DOM
            if (!this.$refs.viewer) {
                return
            }

            // Initial viewer on the first appearance
            if (!this.viewer && typeof StreetSmartApi !== 'undefined') {
                this.viewer = new StreetSmartPanorama(this.$refs.viewer, this.position)
                return
            }

            if (!this.viewer && typeof google !== 'undefined') {
                this.viewer = new GooglePanorama(this.$refs.viewer, this.position)
                return
            }

            // When the viewer is already initialized, only update the position
            if (this.viewer) {
                this.viewer.setPosition(this.position)
            }
        },
        position(value) {
            if (!this.isOpen) {
                // do not update position when the viewer is not open
                return
            }

            if (!this.viewer) {
                // do not update the viewer when it is not initialized
                return
            }

            if (!this.position.marker) {
                return
            }

            this.viewer.setPosition(this.position)
        },
    },
    props: {
        isOpen: Boolean,
        position: Object,
    },
}
</script>

<style>
.resizable-b {
    cursor: ns-resize !important;
}

.resizable-b:before {
    content: '';
    position: absolute;
    background: black;
    width: 100%;
    height: 2px;
    left: 0;
    top: 0;
    bottom: 0;
    margin: auto 0;
}

.mosaic-tile {
    /* Remove black border from StreetSmart */
    margin: 0 !important;
}
</style>

<style scoped>
.buttons {
    position: absolute;
    top: 0;
    right: 0;
    display: flex;
    background: white;
    border-bottom-left-radius: var(--radius-normal);
    box-shadow: var(--shadow-normal);
    overflow: hidden;
    /* Show buttons on top of viewer (buttons) */
    z-index: 3;
}

.viewer {
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: white;
    overflow: hidden;
    /* Show viewer on top of .scale */
    z-index: 2;
}

.buttons .iconbutton:first-child {
    box-sizing: content-box;
    border-right: 1px solid var(--color-grey-50);
}

.iconbutton {
    width: var(--width-button-normal);
    height: var(--width-button-normal);
}

.message {
    display: flex;
    padding: 16px;
    font-size: var(--font-size-small);
    color: var(--color-text-grey);
}
</style>
