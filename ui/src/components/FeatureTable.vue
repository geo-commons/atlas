<template>
  <ExpandButton :title="layer.title" class="feature" v-if="numberMatched > 0">
    <span v-if="error">Er is een fout opgetreden tijdens het laden.</span>
    <span v-if="loading">Bezig met laden...</span>
    <span v-if="!loading && !error && displayProperties.length === 0">Geen weergave beschikbaar.</span>
    <div v-if="!loading && !error && displayProperties.length > 0">
      <button @click="this.downloadCSV">Download</button>
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
    selectedArea: Object
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
  margin: 4px 0 8px;
}
</style>
