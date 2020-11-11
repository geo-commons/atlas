<template>
  <div class="wrapper">
    <button class="iconbutton" v-bind:class="{ isOpen }" @click="toggle" aria-label="Layers"><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M11.99 18.54l-7.37-5.73L3 14.07l9 7 9-7-1.63-1.27zM12 16l7.36-5.73L21 9l-9-7-9 7 1.63 1.27L12 16zm0-11.47L17.74 9 12 13.47 6.26 9 12 4.53z"/></svg></button>
    <div class="layers" v-if="isOpen">
      <ul>
        <li v-for="layer in layers" :key="layer.id">
          {{ layer.id }}
        </li>
      </ul>
    </div>
  </div>
</template>

<script>
export default {
  name: 'LayersPanel',
  data() {
    return {
      isOpen: false
    }
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen
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
