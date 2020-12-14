<template>
  <div class="feature">
    <h2>{{ layer.title }}</h2>
    <div class="details" v-if="features.length > 0">
      <table v-for="feature in features" v-bind:key="feature.id">
          <tr v-for="(value, key) in feature.properties" v-bind:key="key">
            <td>{{ key }}</td>
            <td>{{ value }}</td>
          </tr>
      </table>
    </div>
    <span v-if="features.length === 0">Geen informatie gevonden</span>
  </div>
</template>

<script>
import TileWMS from 'ol/source/TileWMS'
import View from 'ol/View'

export default {
  name: 'FeatureInfo',
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
.feature {
  margin-bottom: 20px;
}

.feature h2 {
  margin: 0 0 8px;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-bold);
}

.details {
  margin: 0 -20px;
  overflow: auto;
}

.details table {
  width: 100%;
  font-size: var(--font-size-small);
}

.details td {
  padding: 4px;
}

.details td:first-child {
  padding-left: 20px;
  color: var(--color-text-grey);
}

.details td:last-child {
  padding-right: 20px;
}
</style>
