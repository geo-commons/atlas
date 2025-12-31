<template>
  <header class="header">
    <div class="nav">
      <a href="/">
        <img
          v-if="config.organization_logo"
          :src="config.organization_logo"
          class="logo"
          :alt="`Logo van ${config.organization_name}`"
        />
        <MenuIcon v-else class="icon" />
      </a>
      <span v-if="config.organization_name" class="organisation-name">Portaal {{ config.organization_name }}</span>
    </div>

    <div v-if="user" class="account">
      <UserMenu current-page="portaal" />
    </div>

    <a v-if="!user" :href="`/atlas/login?next=${encodeURIComponent(nextUrl)}`" class="account">Inloggen</a>
  </header>
</template>

<script>
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";
import MenuIcon from "@/assets/icons/menu-icon.svg";
import UserMenu from "@/components/UserMenu.vue";

export default {
  name: "HeaderPortal",
  components: { MenuIcon, UserMenu },
  computed: {
    ...mapState(useGlobalStore, ["user", "config"]),
    nextUrl() {
      return window.location.pathname;
    },
  },
};
</script>

<style scoped>
header {
  display: flex;
  flex: 0;
  padding: 0 20px;
  z-index: 10;
  background-color: var(--color-white);
  align-items: stretch;
  justify-content: space-between;
  border-bottom: 3px solid var(--color-primary-organization);
  min-height: 80px;
}

@media (min-width: 576px) {
  header {
    padding: 0 32px;
  }
}

.organisation-name {
  display: none;
}

@media (min-width: 576px) {
  .organisation-name {
    display: flex;
    align-items: center;
    font-weight: var(--font-weight-bold);
  }
}

/* Currently the logo is responsible for the height of the header
  with a total height of 55px. */
.logo {
  height: 35px;
  margin-top: 10px;
  margin-bottom: 10px;
}

.nav {
  display: flex;
  align-items: center;
  gap: 24px;
}

.nav > a {
  height: 100%;
  display: flex;
  align-items: center;
  text-decoration: none;
  font-size: var(--font-size-large);
  font-weight: var(--font-weight-bold);
}

.account {
  display: flex;
  align-items: center;
}
</style>
