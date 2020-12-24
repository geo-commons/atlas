<template>
  <div class="wrapper" :class="{ isLarge }" :style="{ display: isOpen ? 'block' : 'none' }">
    <div class="buttons-wrapper ">
      <div class="buttons">
        <button class="iconbutton" :aria-label="isLarge ? 'Verkleinen' : 'Vergroten'" @click="toggleSize">
          <svg v-if="!isLarge" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none"/><path d="M7 14H5v5h5v-2H7v-3zm-2-4h2V7h3V5H5v5zm12 7h-3v2h5v-5h-2v3zM14 5v2h3v3h2V5h-5z"/></svg>
          <svg v-if="isLarge" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none"/><path d="M5 16h3v3h2v-5H5v2zm3-8H5v2h5V5H8v3zm6 11h2v-3h3v-2h-5v5zm2-11V5h-2v5h5V8h-3z"/></svg>
        </button>
        <button class="iconbutton" aria-label="Sluiten" @click="toggle">
          <svg width="14px" height="14px" viewBox="0 0 14 14" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"> <title>Path</title> <g id="Wireframes" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"> <g id="streetview" transform="translate(-985.000000, -413.000000)" fill="#000000" fill-rule="nonzero"> <g id="Group-5" transform="translate(976.000000, 404.000000)"> <polygon id="Path" points="23 10.41 21.59 9 16 14.59 10.41 9 9 10.41 14.59 16 9 21.59 10.41 23 16 17.41 21.59 23 23 21.59 17.41 16"></polygon> </g> </g> </g> </svg>
        </button>
      </div>
    </div>
    <div class="window">
      <div class="viewer" ref="viewer">
        <div v-if="!viewer" class="message">Er is geen panoramaweergave beschikbaar. Controleer de configuratie van Google Maps of StreetSmart.</div>
      </div>
    </div>
  </div>
</template>

<script>
import { GooglePanorama, StreetSmartPanorama } from '../utils/panorama'

export default {
  name: 'PanoramaPanel',
  data() {
    return {
      isLarge: false,
      viewer: null
    }
  },
  methods: {
    toggle() {
      this.$emit('toggle')
    },
    async toggleSize() {
      this.isLarge = !this.isLarge

      await this.$nextTick()

      if (this.viewer && this.viewer instanceof GooglePanorama) {
        // reinitialize GooglePanorama to correctly handle resize
        this.viewer = new GooglePanorama(this.$refs.viewer, this.position)
      }
    },
  },
  watch: {
    isOpen(value) {
      // Make sure the div of the viewer is visible in the DOM
      if (!this.$refs.viewer) {
        return
      }

      // Initial viewer on the first appearance
      if (!this.viewer && typeof StreetSmartApi !== 'undefined') {
        this.viewer = new StreetSmartPanorama(this.$refs.viewer, this.position)
        return
      }

      if (!this.viewer && typeof google !== 'undefined') {
          this.viewer = new GooglePanorama(this.$refs.viewer, this.position)
          return
      }

      // When the viewer is already initialized, only update the position
      if (this.viewer) {
        this.viewer.setPosition(this.position)
      }
    },
    position(value) {
      if (!this.isOpen) {
        // do not update position when the viewer is not open
        return
      }

      if (!this.viewer) {
        // do not update the viewer when it is not initialized
        return
      }

      if (!this.position.marker) {
        return
      }

      this.viewer.setPosition(this.position)
    }
  },
  props: {
    isOpen: Boolean,
    position: Object,
  }
}
</script>

<style scoped>
.wrapper {
  position: absolute;
  bottom: calc(var(--width-button-normal) * 2 + 1px);
  right: 0;
}

.wrapper.isLarge {
  position: fixed;
  width: auto;
  height: auto;
  top: var(--padding-screen);
  left: var(--padding-screen);
  right: var(--padding-screen);
  bottom: calc(var(--padding-screen) + var(--width-button-normal));
  z-index: 2;
}

.window {
  width: 350px;
  max-width: calc(100vw - (var(--padding-screen) * 2));
  height: 300px;
  background: white;
  border-radius: var(--radius-normal);
  border-bottom-right-radius: 0;
  box-shadow: var(--shadow-normal);
  overflow: hidden;
}

.wrapper.isLarge .window {
  width: 100%;
  height: 100%;
}

/* This ensures that the shadow behind .buttons and .window don't fall over each other */
.buttons-wrapper {
  position: absolute;
  bottom: calc((var(--width-button-normal) + 8px) * -1);
  right: -8px;
  overflow: hidden;
  padding: 8px;
  padding-top: 0;
  pointer-events: none;
}

.buttons {
  display: flex;
  background: white;
  border-bottom-left-radius: var(--radius-normal);
  box-shadow: var(--shadow-normal);
  pointer-events: auto;
  overflow: hidden;
}

.buttons .iconbutton:first-child {
  box-sizing: content-box;
  border-right: 1px solid #EAEAEA;
}

.wrapper.isLarge .buttons {
  border-bottom-right-radius: var(--radius-normal);
}

.iconbutton {
  width: var(--width-button-normal);
  height: var(--width-button-normal);
}

.viewer {
  width: 100%;
  height: 100%;
}

.message {
  display: flex;
  align-items: center;
  width: 100%;
  height: 100%;
  padding: 16px;
  font-size: var(--font-size-small);
  color: var(--color-text-grey);
}
</style>
