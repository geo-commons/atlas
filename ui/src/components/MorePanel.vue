<template>
  <div class="wrapper">
    <button
      v-tippy="{ placement: 'auto' }"
      class="iconbutton"
      :class="{ isOpen, isActive: isOpen }"
      content="Opties"
      aria-label="Toon meer opties"
      @click="toggle"
    >
      <EllipsesVertIcon class="icon" />
    </button>
    <transition name="fade">
      <div v-if="isOpen" class="menu tw-min-w-24 tw-max-w-48">
        <ul class="list">
          <li v-if="!user">
            <a :href="`/atlas/login?next=${encodeURIComponent(nextUrl)}`">Inloggen</a>
          </li>

          <li v-if="config.features.portal">
            <a href="/">Portaal</a>
          </li>

          <li><button @click="() => toggleModal('embed')">Embed</button></li>
          <li v-if="map?.features?.showAbout"><button @click="toggleAbout">Informatie</button></li>
          <li v-if="config.features.print">
            <button @click="() => toggleModal('print')">Print</button>
          </li>
          <li><a href="/atlas/docs/" target="_blank" rel="noopener noreferrer">Help</a></li>
          <li v-if="showDisclaimer">
            <a href="/atlas/disclaimer" target="_blank" rel="noopener noreferrer">Disclaimer</a>
          </li>

          <li v-if="user"><hr /></li>
          <li v-if="user && user.is_superuser">
            <a href="/atlas/admin/">Beheer</a>
          </li>
          <li v-if="user">
            <form :action="`/atlas/logout?next=${encodeURIComponent(nextUrl)}`" method="POST">
              <input type="hidden" name="csrfmiddlewaretoken" :value="csrfToken" />
              <button type="submit">Uitloggen</button>
            </form>
          </li>
        </ul>
      </div>
    </transition>
  </div>
</template>

<script>
import Cookies from "js-cookie";
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
    csrfToken() {
      return Cookies.get("csrftoken") || "";
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
