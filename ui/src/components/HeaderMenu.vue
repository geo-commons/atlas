<template>
  <div class="header">
    <div class="nav">
      <a href="/">
        <img
          v-if="config.organization_logo"
          :src="config.organization_logo"
          class="logo"
          :alt="`Logo van ${config.organization_name}`"
        />
        <svg
          v-if="!config.organization_logo"
          xmlns="http://www.w3.org/2000/svg"
          height="24px"
          viewBox="0 0 24 24"
          width="24px"
          fill="#000000"
          class="logo"
        >
          <path d="M0 0h24v24H0V0z" fill="none" />
          <path
            d="M19 5v2h-4V5h4M9 5v6H5V5h4m10 8v6h-4v-6h4M9 17v2H5v-2h4M21 3h-8v6h8V3zM11 3H3v10h8V3zm10 8h-8v10h8V11zm-10 4H3v6h8v-6z"
          />
        </svg>
      </a>
    </div>

    <div v-if="user" class="account">
      <UserMenu current-page="mapviewer" />
    </div>

    <a v-if="!user" :href="`/atlas/login?next=${encodeURIComponent(nextUrl)}`" class="account">Inloggen</a>
  </div>
</template>

<script>
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";
import UserMenu from "@/components/UserMenu.vue";

export default {
  name: "HeaderMenu",
  components: {
    UserMenu,
  },
  computed: {
    ...mapState(useGlobalStore, ["user", "config"]),
    nextUrl() {
      return window.location.pathname;
    },
  },
};
</script>

<style scoped>
.header {
  display: flex;
  padding: 0 20px;
  z-index: 10;
  background-color: var(--color-white);
  align-items: stretch;
  justify-content: space-between;
  box-shadow: 0 1px 0 var(--color-grey-60);
}

@media (min-width: 576px) {
  .header {
    padding: 0 32px;
  }
}

.logo {
  height: 35px;
  margin-top: 10px;
  margin-bottom: 10px;
}

.nav {
  display: flex;
  align-items: center;
}

.nav > * {
  height: 100%;
  display: flex;
  align-items: center;
  text-decoration: none;
  color: black;
  font-size: var(--font-size-large);
  font-weight: var(--font-weight-bold);
}

.account {
  display: flex;
  align-items: center;
}
</style>
