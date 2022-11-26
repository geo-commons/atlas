<template>
    <div class="map-update" v-if="this.data">
        <div class="sidebar">
            <div class="sidebar-content">
                <MapLayers
                    v-if="this.sidebar === 'Layers'"
                    @show-form="() => this.showSidebar('Form')"
                    @change="this.updateLayers"
                    :initialData="this.data"
                />
                <ListPanelAdmin
                    v-if="this.sidebar === 'List'"
                    @show-form="() => this.showSidebar('Form')"
                    @change="this.updateLayers"
                    :initialData="this.data"
                />
                <MapForm
                    v-if="this.sidebar === 'Form'"
                    @show-layers="() => this.showSidebar('Layers')"
                    @show-list="() => this.showSidebar('List')"
                    @delete="this.deleteMap"
                    @submit="this.saveMap"
                    :initialData="this.data"
                />
                <form v-if="this.sidebar === 'Form'" method="POST" @submit="this.deleteMap">
                    <button class="button __alert">Verwijder kaart</button>
                </form>
            </div>
        </div>
        <Map
            ref="map"
            :initialPosition="this.position"
            :initialLayers="this.visibleLayers"
            :user="this.user"
            :features="this.data.features"
            :settings="this.data.settings"
        />
    </div>
</template>

<script>
import Cookies from 'js-cookie'
import { mapState } from 'vuex'

import Map from '../../components/Map/Map'
import MapForm from '../components/MapForm'
import MapLayers from '../components/MapLayers'
import ListPanelAdmin from '../components/ListPanelAdmin'

export default {
    name: 'MapCreateUpdate',
    components: {
        Map,
        MapForm,
        MapLayers,
        ListPanelAdmin,
    },
    created() {
        this.getMap()
    },
    computed: {
        ...mapState({
            position: (state) => state.position,
            layers: (state) => state.layers,
            config: (state) => state.config,
        }),
        visibleLayers() {
            if (this.data.layers) {
                return this.layers
                    .filter(
                        (layer) =>
                            this.data.layers.includes(layer.internal_id) ||
                            (layer.is_base && layer.is_visible)
                    )
                    .map((layer) => {
                        return {
                            ...layer,
                            is_visible: !layer.is_base ? true : layer.is_visible,
                        }
                    })
            }

            return this.layers
        },
    },
    data() {
        return {
            data: null,
            mapPadding: [0, 0, 0, 0],
            selectedArea: null,
            user: null,
            sidebar: 'Form',
        }
    },
    methods: {
        async getMap() {
            if (this.$route.params.id) {
                const result = await fetch(`/atlas/api/v1/maps/${this.$route.params.id}/`, {
                    credentials: 'same-origin',
                    headers: { 'Content-Type': 'application/json' },
                })

                if (!result.ok) {
                    console.error('Could not fetch maps')
                }

                this.data = await result.json()
                return
            }

            this.data = {
                features: {},
                settings: {},
            }
        },
        async saveMap(data) {
            let result

            if (this.$route.params.id) {
                result = await fetch(`/atlas/api/v1/maps/${this.$route.params.id}/`, {
                    method: 'PUT',
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': Cookies.get('csrftoken'),
                    },
                    body: JSON.stringify(data),
                })
            } else {
                result = await fetch(`/atlas/api/v1/maps/`, {
                    method: 'POST',
                    credentials: 'same-origin',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': Cookies.get('csrftoken'),
                    },
                    body: JSON.stringify(data),
                })
            }

            if (result.ok) {
                this.$router.push(`/maps`)
            }
        },
        async deleteMap(e) {
            e.preventDefault()

            const acknowledged = confirm('Weet je zeker dat je de kaart wil verwijderen?')
            if (!acknowledged) {
                return
            }

            const result = await fetch(`/atlas/api/v1/maps/${this.$route.params.id}/`, {
                method: 'DELETE',
                credentials: 'same-origin',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': Cookies.get('csrftoken'),
                },
            })

            if (result.ok) {
                this.$router.push(`/maps`)
            }
        },
        showSidebar(sidebar) {
            this.sidebar = sidebar
        },
        updateLayers(layerIds) {
            this.data.layers = layerIds
        },
    },
}
</script>

<style scoped>
.map-update {
    display: flex;
    height: 100%;
    flex-direction: row;
}

.sidebar-content {
    max-height: 100%;
    overflow-y: auto;
    padding: 16px var(--padding-screen) 80px;
}

.button.__alert {
    margin: 32px auto 0;
}
</style>
