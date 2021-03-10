<template>
    <div class="search-wrapper" :class="{ showBorder }">
      <form class="search" autocomplete="off" method="GET" @submit="onSubmit">
        <button v-if="this.$listeners['show-data-panel']" class="iconbutton toggle-button" type="button" v-tippy='{ placement : "bottom" }' content="Toon data" aria-label="Toon data" @click="showDataPanel">
          <svg xmlns="http://www.w3.org/2000/svg" enable-background="new 0 0 24 24" height="24" viewBox="0 0 24 24" width="24"><g><rect fill="none" height="24" width="24"/><path fill="currentColor" d="M14.17,5L19,9.83V19H5V5L14.17,5L14.17,5 M14.17,3H5C3.9,3,3,3.9,3,5v14c0,1.1,0.9,2,2,2h14c1.1,0,2-0.9,2-2V9.83 c0-0.53-0.21-1.04-0.59-1.41l-4.83-4.83C15.21,3.21,14.7,3,14.17,3L14.17,3z M7,15h10v2H7V15z M7,11h10v2H7V11z M7,7h7v2H7V7z"/></g></svg>
        </button>
        <button v-if="this.$listeners['on-close']" class="iconbutton toggle-button" type="button" v-tippy content="Ga terug" aria-label="Ga terug" @click="onClose">
          <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M19 11H7.83l4.88-4.88c.39-.39.39-1.03 0-1.42-.39-.39-1.02-.39-1.41 0l-6.59 6.59c-.39.39-.39 1.02 0 1.41l6.59 6.59c.39.39 1.02.39 1.41 0 .39-.39.39-1.02 0-1.41L7.83 13H19c.55 0 1-.45 1-1s-.45-1-1-1z"/></svg>
        </button>

        <slot></slot>

        <div class="buttons">
          <button class="iconbutton search-button" type="submit" v-tippy='{ placement : "bottom", theme: "primary" }' content="Zoek" aria-label="Zoek">
            <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path fill="currentColor" d="M15.5 14h-.79l-.28-.27C15.41 12.59 16 11.11 16 9.5 16 5.91 13.09 3 9.5 3S3 5.91 3 9.5 5.91 16 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>
          </button>
        </div>
      </form>
      <slot name="suggestions"></slot>
    </div>
</template>

<script>
export default {
  name: 'Search',
  props: {
    showBorder: Boolean,
  },
  methods: {
    onSubmit(e) {
      e.preventDefault()
      this.$emit('on-submit')
    },
    showDataPanel() {
      this.$emit('show-data-panel')
    },
     onClose() {
      this.$emit('on-close')
    }
  },
}
</script>

<style scoped>
.search-wrapper {
  position: relative;
  width: 100%;
  background: white;
  border-radius: var(--radius-normal);
  overflow: hidden;
  transition: box-shadow .1s;
}

.search-wrapper:not(.showBorder) {
  box-shadow: var(--shadow-normal);
}

.search-wrapper.showBorder {
  box-shadow: 0 0 0 1px var(--color-grey-60);
}

.search {
  display: flex;
  height: var(--width-button-large);
  width: 100%;
}

.search > *,
.buttons > * {
  height: 100%;
}

.search input {
  width: 100%;
  padding-left: 12px;
}

.buttons {
  flex-shrink: 0;
  display: flex;
}

.toggle-button {
  width: var(--width-button-large);
  border-right: 1px solid var(--color-grey-50);
}

.search-button {
  position: relative;
  width: 48px;
}

.search-button > * {
  position: relative;
}

.search-button:not([disabled]):hover {
  background: transparent;
}

.search-button:not([disabled]):active {
  background: transparent;
}

.search-button:before {
  content: '';
  position: absolute;
  top:0;
  left: 0;
  right: 0;
  bottom: 0;
  width: var(--width-button-large);
  height: var(--width-button-large);
  margin: auto;
  border-radius: 50%;
}

.iconbutton:not([disabled]):hover:before {
  background: var(--color-grey-40);
}

.iconbutton:not([disabled]):active:before {
  background: var(--color-grey-50);
}

.search-button:not([disabled]) {
  color: var(--color-primary);
}

.clear-button {
  width: var(--width-button-large);
  border-left: 1px solid var(--color-grey-50);
}

.open-button {
  width: 24px;
  height: var(--width-button-large);
  border-left: 1px solid var(--color-grey-50);
}

.results {
  width: 100%;
  border-top: 1px solid var(--color-grey-50);
  padding: 12px 0;
}

.list a {
  display: block;
  color: #4285F4;
  text-decoration: none;
  padding: 3px 16px;
}

.list a:hover {
  text-decoration: underline;
}
</style>
