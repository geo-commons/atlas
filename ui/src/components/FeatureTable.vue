<template>
    <ExpandButton :title="this.computedTitle" :isOpen="isOpen" class="feature">
        <template v-slot:header>
            <button
                class="iconbutton"
                v-tippy="{ placement: 'right' }"
                content="Download CSV"
                aria-label="Download CSV"
                @click="downloadCSV"
            >
                <svg
                    width="16px"
                    height="16px"
                    viewBox="0 0 16 16"
                    version="1.1"
                    xmlns="http://www.w3.org/2000/svg"
                    xmlns:xlink="http://www.w3.org/1999/xlink"
                >
                    <g id="sketches" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
                        <g
                            id="originals"
                            transform="translate(-340.000000, -166.000000)"
                            fill="#000000"
                            fill-rule="nonzero"
                        >
                            <path
                                d="M342,177 L342,180 L354,180 L354,177 L356,177 L356,180 C356,181.104569 355.104569,182 354,182 L342,182 C340.895431,182 340,181.104569 340,180 L340,177 L342,177 Z M349,166 L349,174.17 L351.59,171.59 L353,173 L348,178 L343,173 L344.41,171.59 L347,174.17 L347,166 L349,166 Z"
                                id="Combined-Shape"
                            ></path>
                        </g>
                    </g>
                </svg>
            </button>
        </template>

        <template v-slot:default>
            <div>
                <span v-if="error">Er is een fout opgetreden tijdens het laden.</span>
                <span v-if="loading">Bezig met laden...</span>
                <span v-if="!loading && !error && displayProperties.length === 0"
                    >Geen weergave beschikbaar.</span
                >
                <div v-if="!loading && !error && displayProperties.length > 0">
                    <Table class="table">
                        <table>
                            <thead>
                                <tr>
                                    <th></th>
                                    <th v-for="property in displayProperties" v-bind:key="property">
                                        {{ property }}
                                    </th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="feature in features" v-bind:key="feature.id">
                                    <td>
                                        <button
                                            v-if="feature.geometry"
                                            class="iconbutton pin-button"
                                            v-tippy="{ placement: 'right' }"
                                            content="Bekijk op kaart"
                                            aria-label="Bekijk op kaart"
                                            @click="() => showFeature(feature)"
                                        >
                                            <svg
                                                width="10px"
                                                height="14px"
                                                viewBox="0 0 10 14"
                                                version="1.1"
                                                xmlns="http://www.w3.org/2000/svg"
                                                xmlns:xlink="http://www.w3.org/1999/xlink"
                                            >
                                                <g
                                                    id="pin"
                                                    stroke="none"
                                                    stroke-width="1"
                                                    fill="none"
                                                    fill-rule="evenodd"
                                                >
                                                    <path
                                                        d="M5,0 C7.5155,0 9.55,2.0345 9.55,4.55 C9.55,7.9625 5,13 5,13 C5,13 0.45,7.9625 0.45,4.55 C0.45,2.0345 2.4845,0 5,0 Z M5,1.3 C3.206,1.3 1.75,2.756 1.75,4.55 C1.75,6.4025 3.648,9.2365 5,10.972 C6.378,9.2235 8.25,6.422 8.25,4.55 C8.25,2.756 6.794,1.3 5,1.3 Z M5,2.925 C5.89746272,2.925 6.625,3.65253728 6.625,4.55 C6.625,5.44746272 5.89746272,6.175 5,6.175 C4.10253728,6.175 3.375,5.44746272 3.375,4.55 C3.375,3.65253728 4.10253728,2.925 5,2.925 Z"
                                                        id="Combined-Shape"
                                                        fill="#000000"
                                                        fill-rule="nonzero"
                                                    ></path>
                                                </g>
                                            </svg>
                                        </button>
                                    </td>
                                    <td v-for="property in displayProperties" v-bind:key="property">
                                        {{ feature.properties[property] }}
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </Table>
                </div>
            </div>
        </template>
    </ExpandButton>
</template>

<script>
import GeoJSON from 'ol/format/GeoJSON'
import { getCenter } from 'ol/extent'

import Table from './Table'
import ExpandButton from './ExpandButton'

export default {
    name: 'FeatureTable',
    components: {
        Table,
        ExpandButton,
    },
    data() {
        return {
            features: [],
            displayProperties: [],
            searchProperties: [],
            loading: false,
            error: false,
            numberMatched: 0,
        }
    },
    props: {
        layer: Object,
        query: String,
        selectedArea: Object,
        isOpen: Boolean,
        filter: Object,
        position: Object,
    },
    mounted() {
        this.fetchFeatures()
        this.fetchSearchProperties()
    },
    watch: {
        query: 'fetchFeatures',
        selectedArea: 'fetchFeatures',
        filter: 'fetchFeatures',
    },
    computed: {
        computedTitle() {
            if (this.numberMatched !== null) {
                return `${this.layer.title} (${this.numberMatched})`
            }

            return this.layer.title
        },
    },
    methods: {
        async fetchFeatures() {
            this.loading = true
            this.error = false

            const params = new URLSearchParams([
                ['service', 'WFS'],
                ['version', '1.0.0'],
                ['request', 'GetFeature'],
                ['typename', this.layer.name],
                ['outputFormat', 'application/json'],
                ['maxFeatures', '5000'],
            ])

            const filters = []

            if (this.query && this.searchProperties.length > 0) {
                filters.push(
                    this.searchProperties
                        .map((key) => `${key} ILIKE '%${this.query}%'`)
                        .join(' OR ')
                )
            }

            if (this.selectedArea) {
                filters.push(
                    `INTERSECTS(geom,POLYGON((${this.selectedArea
                        .getCoordinates()[0]
                        .map((c) => `${c[0]} ${c[1]}`)
                        .join(',')})))`
                )
            }

            if (filters.length > 0) {
                params.set('cql_filter', filters.join(' AND '))
            }

            if (this.filter) {
                params.set('cql_filter', `${this.filter.key} = '${this.filter.value}'`)
            }

            try {
                const url = new URL(this.layer.url)
                url.search = params.toString()

                const result = await fetch(url.toString())
                const data = await result.json()

                this.features = data.features
                this.numberMatched = data.numberMatched

                if (this.displayProperties.length === 0 && data.features.length > 0) {
                    // cache first retrieval of properties into this.displayProperties
                    const fetchedProperties = Object.keys(data.features[0].properties)

                    this.displayProperties =
                        this.layer.display_properties.length > 0
                            ? this.layer.display_properties
                            : fetchedProperties
                }
            } catch (e) {
                console.error(e)
                this.error = true
                this.features = []
                this.displayProperties = []
                this.searchProperties = []
                this.numberMatched = 0
            }

            this.loading = false
        },
        async fetchSearchProperties() {
            if (this.layer.search_properties.length > 0) {
                this.searchProperties = this.layer.search_properties
                return
            }

            const params = new URLSearchParams([
                ['service', 'WFS'],
                ['version', '1.0.0'],
                ['request', 'DescribeFeatureType'],
                ['typename', this.layer.name],
                ['outputFormat', 'application/json'],
            ])

            try {
                const url = new URL(this.layer.url)
                url.search = params.toString()

                const result = await fetch(url.toString())

                const data = await result.json()
                const featureType = data.featureTypes[0]

                // Only search through properties with type string
                const stringProperties = featureType.properties.filter(
                    (p) => p.localType === 'string'
                )

                this.searchProperties = stringProperties.map((p) => p.name)
            } catch (e) {
                console.error(e)
            }
        },
        downloadCSV() {
            const separator = ';'
            const filename = this.layer.title
                .replace(' ', '-')
                .replace(/[^a-z0-9\-]/gi, '')
                .toLowerCase()

            let data =
                this.displayProperties
                    .map((property) => `"${property.replace(/\"/g, '""')}"`)
                    .join(separator) + '\n'

            this.features.forEach((feature) => {
                data +=
                    this.displayProperties
                        .map((property) =>
                            feature.properties[property] !== null
                                ? `"${String(feature.properties[property]).replace(/\"/g, '""')}"`
                                : ''
                        )
                        .join(separator) + '\n'
            })

            const hiddenElement = document.createElement('a')
            hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(data)
            hiddenElement.target = '_blank'
            hiddenElement.download = `${filename}.csv`
            hiddenElement.click()
        },
        showFeature(feature) {
            const geometry = new GeoJSON().readFeature(feature).getGeometry()
            const center = getCenter(geometry.getExtent())

            this.$emit('set-position', {
                ...this.position,
                marker: center,
                center: center,
                zoom: 18,
            })
        },
    },
}
</script>

<style scoped>
.feature:not(:last-child) {
    border-bottom: 1px solid var(--color-grey-50);
}

.table {
    margin: 0 0 24px;
}

.iconbutton {
    width: var(--width-button-normal);
}

.pin-button {
    width: 100%;
    height: 26px;
}

td:first-child {
    width: var(--width-button-large);
    padding: 0 !important;
}
</style>
