<template>
  <div>
    <div class="buttons-wrapper">
      <div class="buttons" :class="{ isOpen: this.panel === 'layers' || this.panel === 'activeLayers', showVisibleLayers: visibleLayers.length > 0 }">
        <button class="iconbutton" :class="{ isActive: this.panel === 'layers' }" @click="() => togglePanel('layers')" v-tippy='{ placement : "top-start" }' content="Alle lagen" aria-label="Toon alle lagen" :aria-expanded="String(this.panel === 'layers')" aria-controls="layers">
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path fill="currentColor" d="M11.99 18.54l-7.37-5.73L3 14.07l9 7 9-7-1.63-1.27zM12 16l7.36-5.73L21 9l-9-7-9 7 1.63 1.27L12 16zm0-11.47L17.74 9 12 13.47 6.26 9 12 4.53z"/></svg>
        </button>

        <button class="iconbutton" :class="{ isActive: this.panel === 'activeLayers' }" @click="() => togglePanel('activeLayers')" v-tippy content="Zichtbare lagen" aria-label="Toon zichtbare lagen" :aria-expanded="String(this.panel === 'activeLayers')" aria-controls="visibleLayers">
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path fill="currentColor" d="M12 6c3.79 0 7.17 2.13 8.82 5.5C19.17 14.87 15.79 17 12 17s-7.17-2.13-8.82-5.5C4.83 8.13 8.21 6 12 6m0-2C7 4 2.73 7.11 1 11.5 2.73 15.89 7 19 12 19s9.27-3.11 11-7.5C21.27 7.11 17 4 12 4zm0 5c1.38 0 2.5 1.12 2.5 2.5S13.38 14 12 14s-2.5-1.12-2.5-2.5S10.62 9 12 9m0-2c-2.48 0-4.5 2.02-4.5 4.5S9.52 16 12 16s4.5-2.02 4.5-4.5S14.48 7 12 7z"/></svg>
        </button>
      </div>

      <transition name="fade">
        <div class="counter visible-layer-counter" v-if="visibleLayers.length > 0">{{ visibleLayers.length }}</div>
      </transition>
    </div>

    <transition name="fade">
      <ul class="layers" v-if="this.panel === 'layers'" id="layers">
        <li>
          <ExpandButton v-for="category in categories" :key="category.id" :title="category.title" class="category-wrapper">
            <template v-slot:button>
              <div v-if="category.layers.filter((layer) => layer.is_visible).length > 0" class="counter layer-counter">{{category.layers.filter((layer) => layer.is_visible).length}}</div>
            </template>
            <template v-slot:default>
              <ul :id="category.id" class="sublayers">
                <li v-for="layer in category.layers" v-bind:key="layer.id">
                  <input type="checkbox" :name="layer.id" :id="layer.id" :checked="layer.is_visible" @change="() => onSelectLayer(layer)" />
                  <label :for="layer.id">{{ layer.title }}</label>
                </li>
              </ul>
            </template>
          </ExpandButton>
        </li>
      </ul>
    </transition>

    <transition name="fade">
      <ul v-if="visibleLayers.length > 0 && this.panel === 'activeLayers'" class="visible-layers" id="visibleLayers">
          <VisibleLayer v-for="layer in visibleLayers" v-bind:key="layer.id" :layer="layer" @set-layer-opacity="setLayerOpacity" @toggle-layer="onSelectLayer" />
        </ul>
    </transition>
  </div>
</template>

<script>
import ExpandButton from './ExpandButton'
import VisibleLayer from './VisibleLayer'

export default {
  name: 'LayersPanel',
  components: {
    ExpandButton,
    VisibleLayer
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
    },
    setLayerOpacity(values) {
      this.$emit('set-layer-opacity', values)
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
    visibleLayers() {
      return this.layers.filter((layer) => layer.category && layer.is_visible)
    }
  },
  props: {
    layers: Array,
  }
}
</script>

<style scoped>
.buttons-wrapper {
  position: relative;
}

.buttons {
  display: flex;
  background: white;
  width: var(--width-button-large);
  overflow: hidden;
  border-radius: var(--radius-normal);
  box-shadow: var(--shadow-normal);
  transition: width .1s ease, border-radius .1s;
}

.buttons.isOpen {
  border-top-left-radius: 0;
  border-top-right-radius: 0;
}

.buttons.showVisibleLayers {
    width: calc(var(--width-button-large) * 2 + 1px);
}

.iconbutton {
  position: relative;
  width: var(--width-button-large);
  height: var(--width-button-large);
}

.iconbutton:not(:last-child) {
  box-sizing: content-box;
  border-right: 1px solid var(--color-grey-50);
}

.visible-layer-counter {
  position: absolute;
  top: 2px;
  left: calc(100% - 8px);
}

.layers,
.visible-layers {
  position: absolute;
  bottom: var(--width-button-large);
  left: 0;
  max-height: calc(100vh - ((var(--width-button-large) * 2) + (var(--padding-screen) * 4)));
  width: calc(var(--width-detail) - (var(--padding-screen) * 2));
  max-width: calc(100vw - (var(--padding-screen) * 3) - var(--width-button-normal));
  overflow-y: auto;
  background: white;
  border-radius: var(--radius-small);
  border-bottom-left-radius: 0;
  box-shadow: var(--shadow-normal);
}

@media (min-width: 650px) {
  .showInfoPanel .layers,
  .showInfoPanel .visible-layers {
    max-width: calc(100vw - (var(--padding-screen) * 3) - var(--width-button-normal) - var(--width-detail));
  }
}

.category-wrapper:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-50);
}

.sublayers {
  padding: 0 0 4px 30px;
}

.sublayers > li {
  position: relative;
}

.sublayers > li > input {
  position: absolute;
  top: 5px;
  left: 0;
  width: 14px;
  height: 14px;
  margin: 0;
}

.sublayers > li > label {
  display: block;
  position: relative;
  width: 100%;
  cursor: pointer;
  padding: 2px 12px 2px 20px;
  user-select: none;
}

.layer-counter {
  margin: 7px 8px 0 4px;
}
</style>
