<template>
  <ExpandButton v-if="features.length > 0" :title="layer.title" class="feature">
    <Table v-if="features.length > 0" class="table">
      <table v-for="feature in features" v-bind:key="feature.id">
        <tbody>
          <tr v-for="(value, key) in feature.properties" v-bind:key="key">
            <td>{{ key }}</td>
            <td>{{ value }}</td>
          </tr>
        </tbody>
      </table>
    </Table>
  </ExpandButton>
</template>

<script>
import Table from './Table'
import TileWMS from 'ol/source/TileWMS'
import View from 'ol/View'
import ExpandButton from './ExpandButton'

export default {
  name: 'FeatureInfo',
  components: {
    Table,
    ExpandButton,
  },
  data() {
    return {
      features: {}
    }
  },
  props: {
    layer: Object,
    position: Object
  },
  mounted() {
    this.fetchFeatures()
  },
  watch: {
    position: 'fetchFeatures'
  },
  methods: {
    async fetchFeatures() {
      const wmsSource = new TileWMS({
          url: this.layer.url,
          servertype: this.layer.server_type,
          params: {
            'LAYERS': this.layer.name,
            'TILED': true
          },
        })

      const view = new View({
        center: this.position.center,
        zoom: this.position.zoom,
      })

      const url = wmsSource.getFeatureInfoUrl(this.position.marker, view.getResolution(), 'EPSG:28992', {
        'INFO_FORMAT': 'application/json'
      })

      try {
        const result = await fetch(url)
        const data = await result.json()
        this.features = data.features
      } catch(e) {
        console.error(e)
      }
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

.table-wrapper td:first-child {
  width: 30%;
  color: var(--color-text-grey);
}
</style>
