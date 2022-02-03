<template>
    <div class="container">
        <div class="sidebar">
            <Layers v-if="this.sidebar === 'Layers'" @show-form="() => this.showSidebar('Form')" />
            <Form v-if="this.sidebar === 'Form'" @show-layers="() => this.showSidebar('Layers')" />
        </div>
        <Map
            ref="map"
            class="map"
            :position="this.position"
            :layers="this.layers"
            :tool="this.tool"
            :selectedArea="this.selectedArea"
            :padding="this.mapPadding"
            :user="this.user"
        />
    </div>
</template>

<script>
import { mapState } from 'vuex'
import Map from '../../../components/Map.vue'
import Form from './Sidebar/Form'
import Layers from './Sidebar/Layers'

export default {
    name: 'MapCreate',
    components: {
        Map,
        Form,
        Layers,
    },
    computed: mapState({
        position: (state) => state.position,
        layers: (state) => state.layers,
        config: (state) => state.config,
    }),
    data() {
        return {
            tool: '',
            mapPadding: [0, 0, 0, 0],
            selectedArea: null,
            user: null,
            sidebar: 'Form',
        }
    },
    methods: {
        showSidebar(sidebar) {
            this.sidebar = sidebar
        },
    },
}
</script>

<style scoped>
.container {
    display: flex;
    height: 100%;
    flex-direction: row;
}

.sidebar {
    width: var(--width-detail);
    z-index: 1;
    box-shadow: var(--shadow-normal);
    padding: var(--padding-screen);
}

.sidebar input {
    width: 100%;
    border: 1px solid var(--color-grey-60);
    padding: 5px;
}

.map {
    height: 100%;
    width: 100%;
}
</style>
