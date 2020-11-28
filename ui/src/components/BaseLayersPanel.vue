<template>
  <div class="wrapper">
    <button class="iconbutton" :class="{ isOpen }" @click="toggle" aria-label="Layers" :aria-expanded="isOpen.toString()" :aria-controls="baseLayers"><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M20.5 3l-.16.03L15 5.1 9 3 3.36 4.9c-.21.07-.36.25-.36.48V20.5c0 .28.22.5.5.5l.16-.03L9 18.9l6 2.1 5.64-1.9c.21-.07.36-.25.36-.48V3.5c0-.28-.22-.5-.5-.5zM10 5.47l4 1.4v11.66l-4-1.4V5.47zm-5 .99l3-1.01v11.7l-3 1.16V6.46zm14 11.08l-3 1.01V6.86l3-1.16v11.84z"/></svg></button>
    <div class="layers" v-if="isOpen" id="baseLayers">
      <ul>
        <li v-for="layer in baseLayers" :key="layer.id">
          <input type="radio" :id="layer.id" name="baseLayer" :checked="layer.is_visible" @change="() => onSelect(layer)">
          <label :for="layer.id">{{ layer.title }}</label>
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'BaseLayersPanel',
  data() {
    return {
      isOpen: false
    }
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen
    },
    onSelect(selectedLayer) {
      this.baseLayers.map((layer) => {
        if (selectedLayer.id === layer.id) {
          this.$emit('toggle-layer', [ layer.id, true ])
        } else {
          this.$emit('toggle-layer', [ layer.id, false ])
        }
      })
    }
  },
  computed: {
    baseLayers() {
      return this.layers.filter((layer) => layer.is_base)
    },
  },
  props: {
    layers: Array,
  }
}
</script>

<style scoped>
.wrapper {
  position: fixed;
  bottom: 92px;
  right: 16px;
}

.iconbutton {
  width: 32px;
  height: 32px;
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
  bottom: 32px;
  right: 0;
  padding: 8px 12px;
  background: white;
  border-radius: 3px;
  border-bottom-left-radius: 0;
  box-shadow: 0 0 4px rgba(0,0,0,.1), 0 0 12px rgba(0,0,0,.15);
}
</style>
