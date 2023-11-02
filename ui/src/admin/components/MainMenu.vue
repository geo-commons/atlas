<template>
  <div class="header container">
    <div class="nav">
      <router-link to="/">
        <MenuIcon class="icon __white" />
        <span v-if="$route.path === '/'" class="dashboard-title color-white">{{ $route.meta.title }}</span>
      </router-link>

      <div v-if="breadcrumb">
        <ChevronRightIcon class="icon __white" />
        <router-link class="breadcrumb" :to="breadcrumb.url">
          <span class="color-white">{{ breadcrumb.displayName }}</span>
        </router-link>
      </div>

      <div v-if="$route.path !== '/'">
        <ChevronRightIcon class="icon __white" />
        <span class="title color-white">{{ $route.meta.title }}</span>
      </div>
    </div>

    <a href="/atlas/admin/logout/" class="logout">
      <LogoutIcon class="icon __white" />
    </a>
  </div>
</template>

<script>
import MenuIcon from "../../assets/icons/menu-icon.svg";
import ChevronRightIcon from "../../assets/icons/chevron-right-icon.svg";
import LogoutIcon from "../../assets/icons/logout-icon.svg";

export default {
  name: "MainMenu",
  components: {
    MenuIcon,
    ChevronRightIcon,
    LogoutIcon,
  },
  computed: {
    breadcrumb() {
      const parentRoute = this.$route.params?.parentRoute;

      if (parentRoute) {
        return this.$route.meta?.breadcrumb[parentRoute];
      }

      return null;
    },
  },
};
</script>

<style scoped>
.header {
  min-height: 56px;
  display: flex;
  align-items: stretch;
  justify-content: space-between;
  box-shadow: 0 1px 0 var(--color-grey-60);
  background: var(--color-primary);
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

.dashboard-title {
  margin-left: 8px;
}

.breadcrumb {
  text-decoration: none;
}

.logout {
  display: flex;
  align-items: center;
}

.color-white {
  color: var(--color-white);
}
</style>
