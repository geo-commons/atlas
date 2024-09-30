<template>
  <div class="header container">
    <router-link to="/" class="dashboard-title">
      <MenuIcon class="icon __white" />
      Atlas Beheerpagina
    </router-link>

    <div class="end-header-wrapper">
      <div class="account-name">{{ user.name }}</div>
      <a href="/atlas/logout" class="logout">
        <LogoutIcon class="icon __white" />
      </a>
    </div>
  </div>
</template>

<script>
import MenuIcon from "../../assets/icons/menu-icon.svg";
import LogoutIcon from "../../assets/icons/logout-icon.svg";
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";

export default {
  name: "MainMenu",
  components: {
    MenuIcon,
    LogoutIcon,
  },
  computed: {
    ...mapState(useGlobalStore, ["user"]),
  },
};
</script>

<style scoped>
.header {
  font-family: var(--font-family-admin);
  min-height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 0 var(--color-grey-60);
  background: var(--color-admin-primary);
}

.dashboard-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: 8px;
  color: var(--color-white);
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-xl);
  text-decoration: none;
}

.logout {
  display: flex;
  align-items: center;
}

.end-header-wrapper {
  display: flex;
  align-items: center;
  gap: 8px;
}

.account-name {
  color: var(--color-white);
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-xl);
}
</style>
