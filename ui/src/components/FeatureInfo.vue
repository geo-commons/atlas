<template>
    <ExpandButton v-if="features.length > 0" :title="layer.title" :isOpen="isOpen" class="feature">
        <Table class="table">
            <table v-for="feature in features" v-bind:key="feature.id">
                <tbody>
                    <tr
                        v-for="property in filterProperties(feature.properties)"
                        v-bind:key="property"
                    >
                        <td>{{ property | capitalize }}</td>
                        <td>
                            <RichValue
                                :dataKey="property"
                                :dataValue="feature.properties[property]"
                            />
                        </td>
                    </tr>
                </tbody>
            </table>
        </Table>
        <div v-for="(linkedData, key) in layer.linked_data" v-bind:key="key" class="linked-data">
            <div v-if="features[0].properties[linkedData.source_key]">
                <b>{{ linkedData.title }}</b>
                <FeatureTable
                    :layer="linkedData"
                    :filter="{
                        key: linkedData.target_key,
                        value: features[0].properties[linkedData.source_key],
                    }"
                    :position="position"
                    @set-position="setPosition"
                />
            </div>
        </div>
    </ExpandButton>
</template>

<script>
import Table from './Table'
import FeatureTable from './FeatureTable'
import TileWMS from 'ol/source/TileWMS'
import View from 'ol/View'
import ExpandButton from './ExpandButton'
import RichValue from './RichValue'

export default {
    name: 'FeatureInfo',
    components: {
        Table,
        ExpandButton,
        FeatureTable,
        RichValue,
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
    methods: {
        async fetchFeatures() {
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
                const result = await fetch(url)
                const data = await result.json()
                this.features = data.features
            } catch (e) {
                console.error(e)
            }
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
    },
}
</script>

<style scoped>
.feature:not(:last-child) {
    border-bottom: 1px solid var(--color-grey-50);
}

.table {
    margin: 4px 0 8px;
}

.linked-data {
    padding: 0 20px;
    margin: 4px 0 8px;
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
