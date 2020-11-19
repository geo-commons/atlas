<template>
  <div class="wrapper">
    <button class="iconbutton" :class="{ isOpen }" @click="toggle" aria-label="Layers" :aria-expanded="isOpen.toString()" :aria-controls="layers"><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M11.99 18.54l-7.37-5.73L3 14.07l9 7 9-7-1.63-1.27zM12 16l7.36-5.73L21 9l-9-7-9 7 1.63 1.27L12 16zm0-11.47L17.74 9 12 13.47 6.26 9 12 4.53z"/></svg></button>
    <div class="layers" v-if="isOpen" id="layers">
      <ul>
        <Category v-for="category in categories" :key="category.id" :category="category" @toggle-layer="toggleLayer">
          {{ category.title }}
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
      isOpen: false
    }
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen
    },
    toggleLayer(props) {
      this.$emit('toggle-layer', props)
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
}

.iconbutton {
  width: 40px;
  height: 40px;
  background: white;
  border-radius: 6px;
  box-shadow: 0 0 4px rgba(0,0,0,.1), 0 0 12px rgba(0,0,0,.15);
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
</style>
