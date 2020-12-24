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
    position: Object,
    selection: Object
  },
  mounted() {
    this.fetchFeatures()
  },
  watch: {
    position: 'fetchFeatures'
  },
  methods: {
    async fetchFeatures() {
      const params = new URLSearchParams([
        ['service', 'WFS'],
        ['version', '1.0.0'],
        ['request', 'GetFeature'],
        ['typename', this.layer.name],
        ['outputFormat', 'application/json'],
        ['maxFeatures', '500'],
      ])

      if (this.position.marker) {
        params.set('cql_filter', `INTERSECTS(geom,POINT(${this.position.marker[0]} ${this.position.marker[1]}))`)
      } else if (this.selection) {
        params.set('cql_filter', `WITHIN(geom,POLYGON((${this.selection.getCoordinates()[0].map(c => `${c[0]} ${c[1]}`).join(',')})))`)
      }

      try {
        const result = await fetch(this.layer.url + params.toString())
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
