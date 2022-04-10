<template>
    <div class="map-update" v-if="this.data">
        <div class="sidebar">
            <div class="content">
                <MapLayers
                    v-if="this.sidebar === 'Layers'"
                    @show-form="() => this.showSidebar('Form')"
                />
                <MapForm
                    v-if="this.sidebar === 'Form'"
                    @show-layers="() => this.showSidebar('Layers')"
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
            :position="this.position"
            :layers="this.layers"
            :tool="this.tool"
            :selectedArea="this.selectedArea"
            :padding="this.mapPadding"
            :user="this.user"
            :features="this.data.features"
        />
    </div>
</template>

<script>
import Cookies from 'js-cookie'
import { mapState } from 'vuex'

import Map from '../../components/Map/Map'
import MapForm from '../components/MapForm'
import MapLayers from '../components/MapLayers'

export default {
    name: 'MapUpdate',
    components: {
        Map,
        MapForm,
        MapLayers,
    },
    created() {
        this.getMap()
    },
    computed: mapState({
        position: (state) => state.position,
        layers: (state) => state.layers,
        config: (state) => state.config,
    }),
    data() {
        return {
            data: null,
            tool: '',
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
    },
}
</script>

<style scoped>
.map-update {
    display: flex;
    height: 100%;
    flex-direction: row;
}

.content {
    max-height: 100%;
    overflow-y: auto;
    padding: 24px var(--padding-screen) 80px;
}

.button.__alert {
    margin: 32px auto 0;
}
</style>
