<template>
    <ExpandButton v-if="features.length > 0" :title="layer.title" :isOpen="isOpen" class="feature">
        <div v-for="feature in features" v-bind:key="feature.id">
            <table-list>
                <table>
                    <tbody>
                        <tr
                            v-for="property in filterProperties(feature.properties)"
                            v-bind:key="property"
                        >
                            <td>{{ layer.friendly_fields && layer.friendly_fields[property] ? layer.friendly_fields[property] : property | capitalize }}</td>
                            <td>
                                <RichValue
                                    :dataKey="property"
                                    :dataValue="feature.properties[property]"
                                />
                            </td>
                        </tr>
                    </tbody>
                </table>
            </table-list>

            <div
                v-for="(linkedData, key) in layer.linked_data"
                v-bind:key="key"
                class="linked-data"
            >
                <div v-if="features[0].properties[linkedData.source_key]">
                    <b>{{ linkedData.title }}</b>
                    <FeatureTable
                        :layer="linkedData"
                        :overallFilter="{
                            key: linkedData.target_key,
                            value: features[0].properties[linkedData.source_key],
                        }"
                        :position="position"
                        @set-position="setPosition"
                    />
                </div>
            </div>

            <div v-for="(template, key) in layer.templates" v-bind:key="key">
                <FeatureInfoTemplate
                    :layer="layer"
                    :template="template"
                    :feature="feature"
                    class="template"
                />
            </div>
        </div>
    </ExpandButton>
</template>

<script>
import nunjucks from 'nunjucks'
import { mapState } from 'vuex'

import FeatureTable from './FeatureTable'
import TableList from './TableList'
import TileWMS from 'ol/source/TileWMS'
import View from 'ol/View'
import ExpandButton from './ExpandButton'
import RichValue from './RichValue'
import FeatureInfoTemplate from './FeatureInfoTemplate'

nunjucks.configure({ autoescaping: true })

export default {
    name: 'FeatureInfo',
    components: {
        TableList,
        FeatureTable,
        ExpandButton,
        RichValue,
        FeatureInfoTemplate,
    },
    data() {
        return {
            features: [],
        }
    },
    props: {
        layer: Object,
        position: Object,
        isOpen: Boolean,
    },
    filters: {
        capitalize: function (value) {
            if (!value) return ''
            // Replace underscores by spaces
            value = value.toString().replace(/_/g, ' ')
            // Uppercase first character
            return value.charAt(0).toUpperCase() + value.slice(1)
        },
    },
    mounted() {
        this.fetchFeatures()
    },
    watch: {
        position: 'fetchFeatures',
    },
    computed: {
        ...mapState({
            user: (state) => state.user,
        }),
    },
    methods: {
        fetchFeatures() {
            if (this.layer.source_type === 'WMS' || this.layer.source_type === 'WMS_WFS') {
                return this.fetchFeaturesFromWMS()
            }

            if (this.layer.source_type === 'WFS') {
                return this.fetchFeaturesFromWFS()
            }
        },
        async fetchFeaturesFromWMS() {
            const wmsSource = new TileWMS({
                url: this.layer.url,
                servertype: this.layer.server_type,
                params: {
                    LAYERS: this.layer.name,
                    TILED: true,
                },
            })

            const view = new View({
                center: this.position.center,
                zoom: this.position.zoom,
            })

            const url = wmsSource.getFeatureInfoUrl(
                this.position.marker,
                view.getResolution(),
                'EPSG:28992',
                {
                    info_format: 'application/json',
                    feature_count: 20,
                }
            )

            try {
                const result = await fetch(url, this.getFetchParameters())
                const data = await result.json()
                this.features = data.features
            } catch (e) {
                console.error(e)
            }
        },
        async fetchFeaturesFromWFS() {
            const params = new URLSearchParams([
                ['service', 'WFS'],
                ['version', '2.0.0'],
                ['request', 'GetFeature'],
                ['typename', this.layer.name],
                ['outputFormat', 'application/json'],
                ['srsname', this.layer.projection],
                ['bbox', `${this.position.marker[0]-10},${this.position.marker[1]-10},${this.position.marker[0]+10},${this.position.marker[1]+10}`],
                ['maxFeatures', '20'],
            ])

            const url = new URL(this.layer.url)
            url.search = params.toString()

            const result = await fetch(
                url.toString(),
                this.getFetchParameters()
            )
            const data = await result.json()

            this.features = data.features
        },
        setPosition(value) {
            this.$store.commit('setPosition', value)
        },
        filterProperties(fetchedProperties) {
            if (this.layer.display_properties.length > 0) {
                return this.layer.display_properties.filter((p) =>
                    Object.keys(fetchedProperties).includes(p)
                )
            }

            return Object.keys(fetchedProperties)
        },
        getFetchParameters() {
            if (
                this.layer.source &&
                this.layer.source.authenticate &&
                this.user &&
                this.user.token
            ) {
                return {
                    headers: { Authorization: `Bearer ${this.user.token}` },
                }
            }

            return {}
        },
    },
}
</script>

<style scoped>
.feature:not(:last-child) {
    border-bottom: 1px solid var(--color-grey-50);
}

.linked-data {
    padding: 0 20px;
    margin: 4px 0 8px;
}

.template {
    padding: 0 20px;
    margin: 4px 0 8px;
}

.template-title {
    display: block;
}

.table-wrapper {
    margin: 4px 0 8px;
}

.table-wrapper + .table-wrapper {
    border-top: 1px solid var(--color-grey-50);
}

.table-wrapper table {
    table-layout: fixed;
}

.table-wrapper td:first-child {
    width: 30%;
    color: var(--color-text-grey);
}

.table-wrapper td:last-child {
    width: 70%;
}
</style>
