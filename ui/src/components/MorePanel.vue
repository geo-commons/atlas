<template>
  <div class="wrapper">
    <button class="iconbutton" :class="{ isOpen }" @click="toggle" aria-label="Meer..."><svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24"><path d="M0 0h24v24H0V0z" fill="none"/><path d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"/></svg></button>
    <transition name="fade">
      <div class="menu" v-if="isOpen">
        <ul class="list">
          <li v-if="!user"><a :href="`/atlas/v3/login?next=${encodeURIComponent(this.nextUrl)}`">Log in</a></li>
          <li v-if="user"><a :href="`/atlas/v3/logout?next=${encodeURIComponent(this.nextUrl)}`">Log uit</a></li>
          <li><a href="/atlas/v3/help" target="_blank">Help</a></li>
          <li><button @click="() => toggleModal('embed')">Embed</button></li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script>
export default {
  name: 'MorePanel',
  data() {
    return {
      isOpen: false
    }
  },
  computed: {
    nextUrl() {
      return window.location.pathname
    }
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen
    },
    toggleModal(modal) {
      this.$emit('toggle-modal', modal)
    }
  },
  props: {
    user: Object,
  }
}
</script>

<style scoped>
.wrapper {
  position: relative;
}

.iconbutton {
  width: var(--width-button-large);
  height: var(--width-button-large);
  background: white;
  border-radius: 50%;
  box-shadow: var(--shadow-normal);
}

.iconbutton.isOpen {
  border-bottom-left-radius: 0;
  border-bottom-right-radius: 0;
}

.menu {
  position: absolute;
  top: var(--width-button-large);
  right: 0;
  padding: 4px 0;
  background: white;
  border-radius: var(--radius-small);
  border-top-right-radius: 0;
  box-shadow: var(--shadow-normal);
  transform: translateY(0);
}

.list a, .list button {
  display: block;
  color: black;
  text-decoration: none;
  padding: 2px 12px;
  font-size: var(--font-size-small);
}

.list a:hover {
  background: #F5F5F5;
}

.list a:active {
  background: #EAEAEA;
}
</style>
