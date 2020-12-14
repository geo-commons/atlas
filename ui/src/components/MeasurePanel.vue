<template>
  <div class="wrapper">
    <button class="iconbutton" :class="{ isActive: this.measure === 'area' }" @click="() => toggleMeasure('area')" aria-label="Oppervlakte meten"><svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24" viewBox="0 0 24 24" width="24"><g><rect fill="none" height="24" width="24"/></g><g><g><path fill="currentColor" d="M17.66,17.66l-1.06,1.06l-0.71-0.71l1.06-1.06l-1.94-1.94l-1.06,1.06l-0.71-0.71l1.06-1.06l-1.94-1.94l-1.06,1.06 l-0.71-0.71l1.06-1.06L9.7,9.7l-1.06,1.06l-0.71-0.71l1.06-1.06L7.05,7.05L5.99,8.11L5.28,7.4l1.06-1.06L4,4v14c0,1.1,0.9,2,2,2 h14L17.66,17.66z M7,17v-5.76L12.76,17H7z"/></g></g></svg></button>
    <button class="iconbutton" :class="{ isActive: this.measure === 'line' }" @click="() => toggleMeasure('line')" aria-label="Afstand meten"><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none"/><path fill="currentColor" d="M21 6H3c-1.1 0-2 .9-2 2v8c0 1.1.9 2 2 2h18c1.1 0 2-.9 2-2V8c0-1.1-.9-2-2-2zm0 10H3V8h2v4h2V8h2v4h2V8h2v4h2V8h2v4h2V8h2v8z"/></svg></button>
  </div>
</template>

<script>
export default {
  name: 'MeasurePanel',
  methods: {
    toggleMeasure(chosenMeasure) {
      this.$emit('set-measure', this.measure !== chosenMeasure ? chosenMeasure : '')
    },
  },
  props: {
    measure: String,
  }
}
</script>

<style scoped>
.wrapper {
  display: flex;
  margin-right: 12px;
  background: white;
  border-radius: var(--radius-small);
  overflow: hidden;
  box-shadow: var(--shadow-normal);
}

.iconbutton {
  width: var(--width-button-large);
  height: var(--width-button-large);
}

.iconbutton:not(:last-child) {
  border-right: 1px solid #EAEAEA;
}
</style>
