<template>
    <SidePanel large :showPanel="showDataPanel">
        <template v-slot:search>
            <div class="flexer">
                <button
                    class="iconbutton close-button"
                    type="button"
                    v-tippy
                    content="Sluit paneel"
                    aria-label="Sluit paneel"
                    @click="toggleDataPanel"
                >
                    <svg
                        xmlns="http://www.w3.org/2000/svg"
                        height="24"
                        viewBox="0 0 24 24"
                        width="24"
                    >
                        <path d="M0 0h24v24H0z" fill="none" />
                        <path
                            d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"
                        />
                    </svg>
                </button>
                <SearchForm :showBorder="true" @on-submit="onSearch" class="data-search">
                    <template v-slot:default>
                        <input
                            ref="queryInput"
                            type="search"
                            name="search"
                            placeholder="Zoek data"
                            autocomplete="off"
                        />
                    </template>
                </SearchForm>
            </div>
        </template>

        <template v-slot:default>
            <FeatureTable
                v-for="visibleLayer in visibleLayers"
                v-bind:key="visibleLayer.id"
                :isOpen="visibleLayers.length === 1"
                :layer="visibleLayer"
                :position="position"
                :selectedArea="selectedArea"
                :query="query"
                :user="user"
                @set-position="setPosition"
                @on-fit="onFit"
            />
        </template>
    </SidePanel>
</template>

<script>
import SidePanel from './SidePanel'
import FeatureTable from './FeatureTable'
import SearchForm from './SearchForm'

const visibleSourceTypes = ['WMS_WFS', 'WFS']

export default {
    name: 'DataPanel',
    components: {
        SidePanel,
        FeatureTable,
        SearchForm,
    },
    methods: {
        onSearch() {
            this.query = this.$refs.queryInput.value
        },
        toggleDataPanel() {
            this.$emit('toggle-data-panel')
        },
        setPosition(value) {
            this.$emit('set-position', value)
        },
        onFit(value) {
            this.$emit('on-fit', value)
        },
    },
    computed: {
        visibleLayers() {
            return this.layers.filter(
                (layer) =>
                    layer.is_visible &&
                    !layer.is_base &&
                    visibleSourceTypes.includes(layer.source_type)
            )
        },
    },
    data() {
        return {
            query: '',
        }
    },
    props: {
        position: Object,
        layers: Array,
        showDataPanel: Boolean,
        selectedArea: Object,
        user: Object,
    },
}
</script>

<style scoped>
.close-button {
    width: var(--width-button-large);
    height: var(--width-button-large);
    border-radius: var(--radius-normal);
    border: 1px solid var(--color-grey-60);
    margin-right: 12px;
}

.flexer {
    display: flex;
}

@media (min-width: 576px) {
    .data-search {
        margin: 0 auto;
        max-width: var(--width-detail);
    }

    .flexer {
        padding-right: calc(var(--width-button-large) + 12px);
    }
}
</style>
