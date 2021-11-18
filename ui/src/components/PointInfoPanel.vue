<template>
    <SidePanel :showPanel="showInfoPanel">
        <template v-slot:search>
            <button
                class="iconbutton close-button"
                type="button"
                v-tippy="{ placement: 'right' }"
                content="Sluit paneel"
                aria-label="Sluit paneel"
                @click="closeInfoPanel"
            >
                <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
                    <path d="M0 0h24v24H0z" fill="none" />
                    <path
                        d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
                    />
                </svg>
            </button>
            <h1>{{ searchQuery }}</h1>
        </template>

        <template v-slot:default>
            <FeatureInfo
                v-for="visibleLayer in visibleLayers"
                :isOpen="visibleLayers.length === 1"
                v-bind:key="visibleLayer.id"
                :layer="visibleLayer"
                :position="position"
                :user="user"
            />
        </template>
    </SidePanel>
</template>

<script>
import SidePanel from './SidePanel'
import FeatureInfo from './FeatureInfo'

export default {
    name: 'MorePanel',
    components: {
        SidePanel,
        FeatureInfo,
    },
    methods: {
        closeInfoPanel() {
            this.searchQuery = ''
            this.$emit('set-position', { ...this.position, marker: null })
        },
    },
    computed: {
        visibleLayers() {
            return this.layers.filter((layer) => layer.is_visible && !layer.is_base)
        },
        searchQuery: {
            get() {
                return this.$store.state.searchQuery
            },
            set(value) {
                this.$store.commit('setSearchQuery', value)
            },
        },
    },
    props: {
        position: Object,
        layers: Array,
        showInfoPanel: Boolean,
        user: Object,
    },
}
</script>

<style scoped>
.open-button {
    position: fixed;
    top: var(--padding-screen);
    z-index: 1;
    width: 24px;
    height: var(--width-button-large);
    background: white;
    border-top-right-radius: var(--radius-small);
    border-bottom-right-radius: var(--radius-small);
    box-shadow: var(--shadow-normal);
}

h1 {
    font-size: var(--font-size-normal);
}

.close-button {
    width: var(--width-button-large);
    height: var(--width-button-large);
    border-radius: var(--radius-normal);
    border: 1px solid var(--color-grey-60);
}
</style>
