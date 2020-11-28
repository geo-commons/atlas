<template>
  <div class="wrapper">
    <button class="iconbutton" :class="{ isOpen: this.panel === 'layers' }" @click="() => togglePanel('layers')" aria-label="Layers" :aria-expanded="String(this.panel === 'layers')" aria-controls="layers"><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M11.99 18.54l-7.37-5.73L3 14.07l9 7 9-7-1.63-1.27zM12 16l7.36-5.73L21 9l-9-7-9 7 1.63 1.27L12 16zm0-11.47L17.74 9 12 13.47 6.26 9 12 4.53z"/></svg></button>
    <div class="layers" v-if="this.panel === 'layers'" id="layers">
      <ul>
        <Category v-for="category in categories" :key="category.id" :category="category">
          <li v-for="layer in category.layers" v-bind:key="layer.id">
            <input type="checkbox" :name="layer.id" :id="layer.id" :checked="layer.is_visible" @change="() => onSelectLayer(layer)" />
            <label :for="layer.id">{{ layer.title }}</label>
          </li>
        </Category>
      </ul>
    </div>
    <button v-if="visibleCategories.length > 0" class="iconbutton" :class="{ isOpen: this.panel === 'activeLayers' }" @click="() => togglePanel('activeLayers')" aria-label="Layers" :aria-expanded="String(this.panel === 'activeLayers')" aria-controls="visibleLayers"><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M12 6c3.79 0 7.17 2.13 8.82 5.5C19.17 14.87 15.79 17 12 17s-7.17-2.13-8.82-5.5C4.83 8.13 8.21 6 12 6m0-2C7 4 2.73 7.11 1 11.5 2.73 15.89 7 19 12 19s9.27-3.11 11-7.5C21.27 7.11 17 4 12 4zm0 5c1.38 0 2.5 1.12 2.5 2.5S13.38 14 12 14s-2.5-1.12-2.5-2.5S10.62 9 12 9m0-2c-2.48 0-4.5 2.02-4.5 4.5S9.52 16 12 16s4.5-2.02 4.5-4.5S14.48 7 12 7z"/></svg></button>
    <div v-if="visibleCategories.length > 0 && this.panel === 'activeLayers'" class="visibleLayers" id="visibleLayers">
      <ul>
        <Category v-for="category in visibleCategories" :key="category.id" :category="category">
          <li v-for="layer in category.layers" v-bind:key="layer.id">
            {{ layer.title }}
          </li>
        </Category>
      </ul>
    </div>
  </div>
</template>

<script>
import Category from './Category'

export default {
  name: 'LayersPanel',
  components: {
    Category
  },
  data() {
    return {
      panel: ''
    }
  },
  methods: {
    togglePanel(selectedPanel) {
      this.panel = selectedPanel !== this.panel ? selectedPanel : ''
    },
    onSelectLayer(selectedLayer) {
      this.$emit('toggle-layer', [ selectedLayer.id, !selectedLayer.is_visible ])
    }
  },
  computed: {
    categories() {
      let categories = {}

      this.layers.forEach((layer) => {
        if (!layer.category) {
          return
        }

        if (categories[layer.category.id]) {
          categories[layer.category.id].layers = [
            ...categories[layer.category.id].layers,
            layer
          ]
        } else {
          categories[layer.category.id] = {
            ...layer.category,
            layers: [layer]
          }
        }
      })

      return Object.values(categories).reverse()
    },
    visibleCategories() {
      let categories = {}

      this.layers.forEach((layer) => {
        if (!layer.category) {
          return
        }

        if (!layer.is_visible) {
          return
        }

        if (categories[layer.category.id]) {
          categories[layer.category.id].layers = [
            ...categories[layer.category.id].layers,
            layer
          ]
        } else {
          categories[layer.category.id] = {
            ...layer.category,
            layers: [layer]
          }
        }
      })

      return Object.values(categories).reverse()
    }
  },
  props: {
    layers: Array,
  }
}
</script>

<style scoped>
.wrapper {
  position: fixed;
  bottom: 16px;
  left: 16px;
  display: flex;
  border-radius: 6px;
  box-shadow: 0 0 4px rgba(0,0,0,.1), 0 0 12px rgba(0,0,0,.15);
}

.iconbutton {
  width: 40px;
  height: 40px;
  background: white;
}

.iconbutton:not(:last-child) {
  border-right: 1px solid #EAEAEA;
}

.iconbutton.isOpen {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.layers {
  position: absolute;
  bottom: 40px;
  left: 0;
  padding: 8px 12px;
  background: white;
  border-radius: 3px;
  border-bottom-left-radius: 0;
  box-shadow: 0 0 4px rgba(0,0,0,.1), 0 0 12px rgba(0,0,0,.15);
}

.visibleLayers {
  position: absolute;
  bottom: 40px;
  left: 40px;
  padding: 8px 12px;
  background: white;
  border-radius: 3px;
  border-bottom-left-radius: 0;
  box-shadow: 0 0 4px rgba(0,0,0,.1), 0 0 12px rgba(0,0,0,.15);
}
</style>
