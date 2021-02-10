<template>
  <ExpandButton :title="layer.title" :isOpen="isOpen" class="feature" v-if="numberMatched > 0">
    <template v-slot:header>
      <button class="iconbutton" v-tippy='{ placement : "right" }' content="Download CSV" aria-label="Download CSV" @click="downloadCSV">
        <svg width="16px" height="16px" viewBox="0 0 16 16" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"> <g id="sketches" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"> <g id="originals" transform="translate(-340.000000, -166.000000)" fill="#000000" fill-rule="nonzero"> <path d="M342,177 L342,180 L354,180 L354,177 L356,177 L356,180 C356,181.104569 355.104569,182 354,182 L342,182 C340.895431,182 340,181.104569 340,180 L340,177 L342,177 Z M349,166 L349,174.17 L351.59,171.59 L353,173 L348,178 L343,173 L344.41,171.59 L347,174.17 L347,166 L349,166 Z" id="Combined-Shape"></path> </g> </g> </svg>
      </button>
    </template>

    <template v-slot:default>
      <span v-if="error">Er is een fout opgetreden tijdens het laden.</span>
      <span v-if="loading">Bezig met laden...</span>
      <span v-if="!loading && !error && displayProperties.length === 0">Geen weergave beschikbaar.</span>
      <div v-if="!loading && !error && displayProperties.length > 0">
        <Table class="table">
          <table>
            <thead>
              <tr>
                <th v-for="property in displayProperties" v-bind:key="property">
                  {{ property }}
                </th>
              </tr>
            </thead>
            <tbody>
              <tr v-for="feature in features" v-bind:key="feature.id">
                <td v-for="property in displayProperties" v-bind:key="property">
                  {{ feature.properties[property] }}
                </td>
              </tr>
            </tbody>
          </table>
        </Table>
      </div>
    </template>
  </ExpandButton>
</template>

<script>
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
      numberMatched: 0
    }
  },
  props: {
    layer: Object,
    query: String,
    selectedArea: Object,
    isOpen: Boolean
  },
  mounted() {
    this.fetchFeatures()
  },
  watch: {
    position: 'fetchFeatures',
    query: 'fetchFeatures',
    selectedArea: 'fetchFeatures'
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
        ['maxFeatures', '500'],
      ])

      const filters = []

      if (this.query && this.searchProperties.length > 0) {
        filters.push(this.searchProperties.map((key) => `${key} ILIKE '%${this.query}%'`).join(' OR '))
      }

      if (this.selectedArea) {
        filters.push(`WITHIN(geom,POLYGON((${this.selectedArea.getCoordinates()[0].map(c => `${c[0]} ${c[1]}`).join(',')})))`)
      }

      if (filters.length > 0) {
        params.set('cql_filter', filters.join(' AND '))
      }

      try {
        const result = await fetch(this.layer.url + params.toString())
        const data = await result.json()

        this.features = data.features
        this.numberMatched = data.numberMatched

        if (this.displayProperties.length === 0 && data.features.length > 0) {
          // cache first retrieval of properties into this.properties
          const fetchedProperties = Object.keys(data.features[0].properties)
          this.displayProperties = this.layer.display_properties.length > 0 ? this.layer.display_properties.filter((p) => fetchedProperties.includes(p)) : fetchedProperties
          this.searchProperties = this.layer.search_properties.filter((p) => fetchedProperties.includes(p))
        }
      } catch(e) {
        console.error(e)
        this.error = true
        this.features = []
        this.displayProperties = []
        this.searchProperties = []
        this.numberMatched = 0
      }

      this.loading = false
    },
    downloadCSV() {
      const filename = this.layer.title.replace(' ', '-').replace(/[^a-z0-9\-]/gi, '').toLowerCase()

      let data = this.displayProperties.map((property) => `"${property.replace(/\"/g, "\"\"")}"`).join(',') + '\n'

      this.features.forEach((feature) => {
        data += this.displayProperties.map((property) => feature.properties[property] !== null ? `"${String(feature.properties[property]).replace(/\"/g, "\"\"")}"` : "").join(',') + '\n'
      })

      const hiddenElement = document.createElement('a')
      hiddenElement.href = 'data:text/csv;charset=utf-8,' + encodeURI(data)
      hiddenElement.target = '_blank'
      hiddenElement.download = `${filename}.csv`
      hiddenElement.click()
    }
  }
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
</style>
