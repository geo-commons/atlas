<template>
  <ExpandButton v-if="feature" :title="''" :isOpen="isOpen" class="feature">
    <img v-if="feature.properties && feature.properties.featuredImage" :src="feature.properties.featuredImage" class="featured-image" />
    <div class="content">
    <div v-if="feature.properties" class="special-properties">
      <h1 v-if="feature.properties.title">{{ feature.properties.title }}</h1>
      <p v-if="feature.properties.description" class="markdown">
        <vue-simple-markdown :source="feature.properties.description" />
      </p>
    </div>
    <div v-for="displayProperty in displayProperties" v-bind:key="displayProperty" class="properties">
      <div v-if="feature.properties[displayProperty]" class="property">
        <strong>{{ displayProperty|capitalize }}</strong>
        <RichValue :dataKey="displayProperty" :dataValue="feature.properties[displayProperty]" />
      </div>
    </div>
    <div v-for="(linkedData, key) in layer.linked_data" v-bind:key="key" class="linked-data">
      <div v-if="features[0].properties[linkedData.source_key]">
        <strong>{{ linkedData.title }}</strong>
        <FeatureTable
          :layer="linkedData"
          :filter="{ key: linkedData.target_key, value: features[0].properties[linkedData.source_key] }"
          :position="position"
          @set-position="setPosition"
        />
      </div>
    </div>
    <div v-if="feature.properties" class="special-properties">
      <div v-if="feature.properties.link" class="link">
        <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" width="24px"  height="24px" fill="#4285F4"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6-6-6z"/></svg>
        <vue-simple-markdown :source="feature.properties.link" class="markdown" />
      </div>
    </div>
    </div>
  </ExpandButton>
</template>

<script>
const specialProperties = ['title', 'description', 'link', 'featuredImage', 'icon']

import FeatureTable from './FeatureTable'
import TileWMS from 'ol/source/TileWMS'
import View from 'ol/View'
import ExpandButton from './ExpandButton'
import RichValue from './RichValue'

export default {
  name: 'FeatureInfo',
  components: {
    ExpandButton,
    FeatureTable,
    RichValue
  },
  data() {
    return {
      feature: {},
      displayProperties: []
    }
  },
  props: {
    layer: Object,
    position: Object,
    isOpen: Boolean
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

        if (data.features.length > 0) {
          const fetchedProperties = Object.keys(data.features[0].properties)
          this.displayProperties = this.layer.display_properties.length > 0 ? this.layer.display_properties.filter((p) => fetchedProperties.includes(p)) : fetchedProperties
          this.displayProperties = this.displayProperties.filter((p) => !specialProperties.includes(p))
          this.feature = data.features[0]

          if (this.feature.properties.featuredImage) {
            this.$emit('on-featured-image', true)
          }
        }
      } catch(e) {
        console.error(e)
      }
    },
    setPosition(value) {
      this.$store.commit('setPosition', value)
    }
  },
  filters: {
    capitalize: function (value) {
      if (!value) return ''
      value = value.toString()
      return value.charAt(0).toUpperCase() + value.slice(1)
    }
  }
}
</script>

<style scoped>
.content {
  padding: 16px 0;
}

.feature:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-50);
}

.featured-image {
  width: 100%;
}

.special-properties {
  padding: 0 var(--padding-screen);;
}

.special-properties h1 {
  margin: 0 0 8px;
  font-size: var(--font-size-large);
  font-weight: var(--font-weight-normal);
  font-weight: var(--font-weight-bold);
}

.special-properties p {
  margin: 0 0 20px;
}

.feature strong {
  display: block;
  font-weight: var(--font-weight-bold);
  margin-bottom: 4px;
}

.properties {
  padding: 0 var(--padding-screen);;
}

.property {
  margin-bottom: 20px;
}

.table {
  margin: 4px 0 8px;
  table-layout: fixed;
}

.linked-data {
  padding: 0 var(--padding-screen);;
  margin: 4px 0 8px;
}

.table-wrapper >>> td:first-child {
  width: 30%;
  color: var(--color-text-grey);
}

.table-wrapper >>> table {
  width: 100%;
  table-layout: fixed;
}

.table-wrapper >>> td {
  word-wrap: break-word;
}

.table-wrapper >>> img {
  width: 100%;
}

.link {
  display: flex;
  align-items: center;
}

.markdown >>> a {
  display: block;
  color: #4285F4;
  text-decoration: none;
}

.markdown >>> a:hover {
  text-decoration: underline;
}

</style>
