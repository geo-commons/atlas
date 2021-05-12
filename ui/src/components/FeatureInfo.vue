<template>
  <ExpandButton v-if="feature" :title="''" :isOpen="isOpen" class="feature">
    <img v-if="feature.properties && feature.properties.featuredImage" :src="feature.properties.featuredImage" class="featured-image" />
    <div class="content">
    <div v-if="feature.properties" class="properties">
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
    <div v-if="feature.properties">
      <div v-if="feature.properties.link" class="link">
        <svg width="20px" height="20px" viewBox="0 0 20 20" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"> <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"> <g id="public_black_24dp" transform="translate(-2.000000, -2.000000)" fill="currentColor" fill-rule="nonzero"> <path d="M12,2 C6.48,2 2,6.48 2,12 C2,17.52 6.48,22 12,22 C17.52,22 22,17.52 22,12 C22,6.48 17.52,2 12,2 Z M4,12 C4,11.39 4.08,10.79 4.21,10.22 L8.99,15 L8.99,16 C8.99,17.1 9.89,18 10.99,18 L10.99,19.93 C7.06,19.43 4,16.07 4,12 Z M17.89,17.4 C17.63,16.59 16.89,16 15.99,16 L14.99,16 L14.99,13 C14.99,12.45 14.54,12 13.99,12 L7.99,12 L7.99,10 L9.99,10 C10.54,10 10.99,9.55 10.99,9 L10.99,7 L12.99,7 C14.09,7 14.99,6.1 14.99,5 L14.99,4.59 C17.92,5.77 20,8.65 20,12 C20,14.08 19.19,15.98 17.89,17.4 Z" id="Shape"></path> </g> </g> </svg>
        <vue-simple-markdown :source="feature.properties.link" class="markdown" />
        <svg width="14px" height="14px" viewBox="0 0 14 14" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"> <g id="Page-1" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"> <g id="open_in_new_black_18dp-(1)" transform="translate(-2.000000, -2.000000)" fill="#000000" fill-rule="nonzero"> <path d="M14.25,14.25 L3.75,14.25 L3.75,3.75 L9,3.75 L9,2.25 L3.75,2.25 C2.9175,2.25 2.25,2.925 2.25,3.75 L2.25,14.25 C2.25,15.075 2.9175,15.75 3.75,15.75 L14.25,15.75 C15.075,15.75 15.75,15.075 15.75,14.25 L15.75,9 L14.25,9 L14.25,14.25 Z M10.5,2.25 L10.5,3.75 L13.1925,3.75 L5.82,11.1225 L6.8775,12.18 L14.25,4.8075 L14.25,7.5 L15.75,7.5 L15.75,2.25 L10.5,2.25 Z" id="Shape"></path> </g> </g> </svg>
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
.feature:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-50);
}

.featured-image {
  width: 100%;
  margin-top: calc(var(--padding-screen) * -1 + var(--width-button-large) * -1);
}

.content {
  padding: 16px 0;
}

.properties {
  padding: 0 var(--padding-screen);
}

.property {
  margin-bottom: 20px;
}

.properties h1 {
  margin: 0 0 8px;
  font-size: var(--font-size-large);
  font-weight: var(--font-weight-normal);
  font-weight: var(--font-weight-bold);
}

.properties p {
  margin: 0 0 20px;
}

.feature strong {
  display: block;
  font-weight: var(--font-weight-bold);
  margin-bottom: 4px;
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
  border-top: 1px solid var(--color-grey-50);
  border-bottom: 1px solid var(--color-grey-50);
  padding: 9px var(--padding-screen);
  color: var(--color-primary);
}

.link svg:first-child {
  margin-right: 8px;
}

.link svg:last-child {
  margin-left: auto;
}

.markdown >>> a {
  display: block;
  color: var(--color-primary);
  text-decoration: none;
}

.markdown >>> a:hover {
  text-decoration: underline;
}

</style>
