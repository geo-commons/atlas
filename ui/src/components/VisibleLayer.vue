<template>
    <li class="layer-wrapper">
        <ExpandButton :title="layer.title">
            <template v-slot:header>
                <div class="buttons">
                    <input
                        v-if="showSlider"
                        class="opacity-slider"
                        type="range"
                        id="opacity"
                        name="opacity"
                        min="0"
                        max="100"
                        step="10"
                        :aria-label="`Doorzichtigheid van laag ${layer.title} instellen`"
                        :value="layer.opacity * 100"
                        @change="(e) => changeLayerOpacity(layer.id, e.target.value / 100)"
                    />
                    <button
                        class="iconbutton"
                        :class="{ isActive: showSlider }"
                        v-tippy
                        content="Doorzichtigheid"
                        aria-label="Toon doorzichtigheid schuifregelaar"
                        @click="toggleSlider"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            height="24"
                            viewBox="0 0 24 24"
                            width="24"
                        >
                            <path d="M24 0H0v24h24V0zm0 0H0v24h24V0zM0 24h24V0H0v24z" fill="none" />
                            <path
                                fill="currentColor"
                                d="M17.66 8L12 2.35 6.34 8C4.78 9.56 4 11.64 4 13.64s.78 4.11 2.34 5.67 3.61 2.35 5.66 2.35 4.1-.79 5.66-2.35S20 15.64 20 13.64 19.22 9.56 17.66 8zM6 14c.01-2 .62-3.27 1.76-4.4L12 5.27l4.24 4.38C17.38 10.77 17.99 12 18 14H6z"
                            />
                        </svg>
                    </button>
                    <input
                        class="opacity-input"
                        type="number"
                        :name="`${layer.id}-opacity`"
                        :id="`${layer.id}-opacity`"
                        :aria-label="`Doorzichtigheid van laag ${layer.title} instellen`"
                        min="0"
                        max="100"
                        step="10"
                        :value="layer.opacity * 100"
                        @change="(e) => changeLayerOpacity(layer.id, e.target.value / 100)"
                    />
                    <button
                        class="iconbutton"
                        v-tippy="{ placement: 'right' }"
                        content="Sluit"
                        aria-label="Sluit laag"
                        @click="toggleLayer"
                    >
                        <svg
                            xmlns="http://www.w3.org/2000/svg"
                            height="24"
                            viewBox="0 0 24 24"
                            width="24"
                        >
                            <path d="M0 0h24v24H0V0z" fill="none" opacity=".87" />
                            <path
                                d="M12 2C6.47 2 2 6.47 2 12s4.47 10 10 10 10-4.47 10-10S17.53 2 12 2zm0 18c-4.41 0-8-3.59-8-8s3.59-8 8-8 8 3.59 8 8-3.59 8-8 8zm3.59-13L12 10.59 8.41 7 7 8.41 10.59 12 7 15.59 8.41 17 12 13.41 15.59 17 17 15.59 13.41 12 17 8.41z"
                            />
                        </svg>
                    </button>
                </div>
            </template>

            <template v-slot:default>
                <div class="content">
                    <img :src="legendImageUrl" :alt="`Legenda voor laag ${layer.title}`" />
                </div>
            </template>
        </ExpandButton>
    </li>
</template>

<script>
import TileWMS from 'ol/source/TileWMS'
import View from 'ol/View'
import ExpandButton from './ExpandButton'

export default {
    name: 'VisibleLayer',
    components: {
        ExpandButton,
    },
    props: {
        layer: Object,
    },
    data() {
        return {
            showSlider: false,
        }
    },
    computed: {
        legendImageUrl() {
            const wmsSource = new TileWMS({
                url: this.layer.url,
                servertype: this.layer.server_type,
                params: {
                    LAYERS: this.layer.name,
                    TILED: true,
                },
            })

            const view = new View()
            return wmsSource.getLegendUrl(view.getResolution())
        },
    },
    methods: {
        toggleSlider() {
            this.showSlider = !this.showSlider
        },
        changeLayerOpacity(layerId, opacity) {
            this.$emit('set-layer-opacity', [layerId, opacity])
        },
        toggleLayer() {
            this.$emit('toggle-layer', this.layer)
        },
    },
}
</script>

<style scoped>
.layer-wrapper:not(:last-child) {
    border-bottom: 1px solid var(--color-grey-50);
}

.opacity-input {
    width: 22px;
    flex-shrink: 0;
    padding: 0;
    font-size: 12px;
    font-weight: var(--font-weight-bold);
}

.opacity-input::-webkit-inner-spin-button {
    -webkit-appearance: none;
    margin: 0;
}

.opacity-input[type='number'] {
    -moz-appearance: textfield;
}

.opacity-slider {
    flex-shrink: 0;
    width: 80px;
    margin: 0;
}

.iconbutton {
    width: var(--width-button-normal);
}

.content {
    padding: 4px 8px 4px;
    overflow-x: auto;
}

.buttons {
    height: var(--width-button-normal);
    display: flex;
}
</style>
