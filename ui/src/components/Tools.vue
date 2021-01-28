<template>
  <div class="wrapper">
    <div class="buttons" :class="{ showMeasureMenu }">
      <button class="iconbutton" :class="{ isActive: tool === 'SELECT_AREA' }" @click="toggleSelectArea" v-tippy='{ placement : "bottom" }' content="Selecteer gebied" aria-label="Selecteer gebied">
        <svg width="18px" height="18px" viewBox="0 0 18 18" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"> <title>Shape</title> <g id="Symbols" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd"> <g id="controls-top-right/loggedin" transform="translate(-11.000000, -11.000000)" fill="currentColor" fill-rule="nonzero"> <g id="highlight_alt-24px" transform="translate(8.000000, 8.000000)"> <path d="M17,5 L15,5 L15,3 L17,3 L17,5 Z M15,21 L17,21 L17,18.41 L19.59,21 L21,19.59 L18.41,17 L21,17 L21,15 L15,15 L15,21 Z M19,9 L21,9 L21,7 L19,7 L19,9 Z M19,13 L21,13 L21,11 L19,11 L19,13 Z M11,21 L13,21 L13,19 L11,19 L11,21 Z M7,5 L9,5 L9,3 L7,3 L7,5 Z M3,17 L5,17 L5,15 L3,15 L3,17 Z M5,21 L5,19 L3,19 C3,20.1 3.9,21 5,21 Z M19,3 L19,5 L21,5 C21,3.9 20.1,3 19,3 Z M11,5 L13,5 L13,3 L11,3 L11,5 Z M3,9 L5,9 L5,7 L3,7 L3,9 Z M7,21 L9,21 L9,19 L7,19 L7,21 Z M3,13 L5,13 L5,11 L3,11 L3,13 Z M3,5 L5,5 L5,3 C3.9,3 3,3.9 3,5 Z" id="Shape"></path> </g> </g> </g> </svg>
      </button>

      <button class="iconbutton" :class="{ isActive: tool === 'MEASURE_AREA' || tool === 'MEASURE_LINE' }" @click="toggleMeasure" v-tippy='{ placement : "bottom" }' content="Opmeten" aria-label="Opmeten">
        <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none"/><path fill="currentColor" d="M21 6H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 10H3V8h2v4h2V8h2v4h2V8h2v4h2V8h2v4h2V8h2v8z"/></svg>
      </button>
    </div>

     <transition name="fade">
      <div class="menu" v-if="showMeasureMenu">
        <ul class="list">
          <li>
            <button @click="() => setMeasureTool('MEASURE_AREA')" aria-label="Meet oppervlakte">Oppervlakte</button>
          </li>
          <li>
            <button @click="() => setMeasureTool('MEASURE_LINE')" aria-label="Meet afstand">Afstand</button>
          </li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'Tools',
  data() {
    return {
      showMeasureMenu: false
    }
  },
  methods: {
    toggleMeasure() {
      if (this.tool === 'MEASURE_AREA' || this.tool === 'MEASURE_LINE') {
        this.$emit('set-tool', '')
      } else {
        this.showMeasureMenu = !this.showMeasureMenu
      }
    },
    toggleSelectArea() {
      if (this.tool !== 'SELECT_AREA') {
        this.$emit('set-tool', 'SELECT_AREA')
      } else {
        // toggle off when the user is currently selecting an area
        this.$emit('set-tool', '')
        this.$emit('set-selected-area', null)
      }
    },
    setMeasureTool(chosenTool) {
      this.$emit('set-tool', this.tool !== chosenTool ? chosenTool : '')
      this.showMeasureMenu = false
    },
  },
  props: {
    tool: String
  }
}
</script>

<style scoped>
.wrapper {
  position: relative;
  margin-right: 12px;
}

.buttons {
  display: flex;
  background: white;
  overflow: hidden;
  border-radius: var(--radius-normal);
  box-shadow: var(--shadow-normal);
}

.buttons.showMeasureMenu {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}

.iconbutton {
  width: var(--width-button-large);
  height: var(--width-button-large);
}

.iconbutton:not(:last-child) {
  border-right: 1px solid var(--color-grey-50);
}

.iconbutton.isActive {
  color: var(--color-primary);
}

.menu {
  position: absolute;
  top: var(--width-button-large);
  right: 0;
}
</style>