<template>
  <li class="category-wrapper">
    <button class="category" @click="toggle" :aria-expanded="isOpen.toString()" :aria-controls="category.id">
      <svg v-if="!isOpen" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none"/><path d="M10 6L8.59 7.41 13.17 12l-4.58 4.59L10 18l6-6z"/></svg>
      <svg v-if="isOpen" xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0z" fill="none"/><path d="M16.59 8.59L12 13.17 7.41 8.59 6 10l6 6 6-6z"/></svg>
      {{ category.title }}
    </button>
    <ul :id="category.id" v-if="isOpen" class="layers">
      <slot />
    </ul>
  </li>
</template>

<script>
export default {
  name: 'Category',
  data() {
    return {
      isOpen: false
    }
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen
    },
  },
  props: {
    category: Object,
  }
}
</script>

<style scoped>
.category-wrapper:not(:last-child) {
  border-bottom: 1px solid var(--color-grey-50);
}

.category {
  display: flex;
  align-items: center;
  height: 30px;
  width: 100%;
  padding: 0 12px 0 4px;
}

.category > svg {
  margin-right: 2px;
}

.layers {
  margin-left: 30px;
}

.layers > li {
  position: relative;
}

.layers > li:last-child {
  margin-bottom: 4px;
}

.layers > li > input {
  position: absolute;
  top: 5px;
  left: 0;
  width: 14px;
  height: 14px;
  margin: 0;
}

.layers > li > label {
  display: block;
  position: relative;
  width: 100%;
  cursor: pointer;
  padding: 2px 12px 2px 20px;
  user-select: none;
}
</style>
