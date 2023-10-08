<template>
  <div class="wrapper">
    <button v-tippy="{ placement: 'bottom' }" class="iconbutton" :class="{ isOpen }" content="Opties" aria-label="Toon meer opties" @click="toggle">
      <svg xmlns="http://www.w3.org/2000/svg" height="24" viewBox="0 0 24 24" width="24">
        <path d="M0 0h24v24H0V0z" fill="none" />
        <path
          d="M12 8c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zm0 2c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2zm0 6c-1.1 0-2 .9-2 2s.9 2 2 2 2-.9 2-2-.9-2-2-2z"
        />
      </svg>
    </button>
    <transition name="fade">
      <div v-if="isOpen" class="menu">
        <ul class="list">
          <li v-if="!user">
            <a :href="`/atlas/login?next=${encodeURIComponent(nextUrl)}`">Log in</a>
          </li>
          <li v-if="user && !config.features.portal">
            <a :href="`/atlas/logout?next=${encodeURIComponent(nextUrl)}`">Log uit</a>
          </li>
          <li><button @click="() => toggleModal('embed')">Embed</button></li>
          <li v-if="config.features.print">
            <button @click="() => toggleModal('print')">Print</button>
          </li>
          <li><a href="/atlas/help" target="_blank">Help</a></li>
          <li v-if="showDisclaimer">
            <a href="/atlas/disclaimer" target="_blank">Disclaimer</a>
          </li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script>
import { mapState } from "vuex";

export default {
  name: "MorePanel",
  props: {
    user: Object,
    showDisclaimer: Boolean,
  },
  data() {
    return {
      isOpen: false,
    };
  },
  computed: {
    nextUrl() {
      return window.location.pathname;
    },
    ...mapState({
      config: (state) => state.config,
    }),
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen;
    },
    toggleModal(modal) {
      this.$emit("toggle-modal", modal);
    },
  },
};
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
}
</style>
