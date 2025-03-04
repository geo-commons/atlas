<template>
  <div class="wrapper">
    <button
      v-tippy="{ placement: 'bottom' }"
      class="iconbutton"
      :class="{ isOpen, isActive: isOpen }"
      content="Opties"
      aria-label="Toon meer opties"
      @click="toggle"
    >
      <EllipsesVertIcon class="icon" />
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
          <li v-if="map?.features?.showAbout"><button @click="toggleAbout">Informatie</button></li>
          <li v-if="config.features.print">
            <button @click="() => toggleModal('print')">Print</button>
          </li>
          <li><a href="/atlas/docs/" target="_blank">Help</a></li>
          <li v-if="showDisclaimer">
            <a href="/atlas/disclaimer" target="_blank">Disclaimer</a>
          </li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script>
import EllipsesVertIcon from "../assets/icons/ellipsis-vert-icon.svg";
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";

export default {
  name: "MorePanel",
  components: {
    EllipsesVertIcon,
  },
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
    ...mapState(useGlobalStore, ["config", "map"]),
  },
  methods: {
    toggle() {
      this.isOpen = !this.isOpen;
    },
    toggleModal(modal) {
      this.$emit("toggle-modal", modal);
      this.isOpen = false;
    },
    toggleAbout() {
      this.$emit("toggle-about");
      this.isOpen = false;
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
