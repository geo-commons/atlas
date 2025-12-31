<template>
  <div class="header container tw-bg-indigo-600">
    <router-link to="/" class="dashboard-title">
      <MenuIcon class="icon __white" />
      Atlas beheer
    </router-link>

    <UserMenu current-page="beheer" />
  </div>
</template>

<script setup lang="ts">
import MenuIcon from "../../assets/icons/menu-icon.svg";
import UserMenu from "@/components/UserMenu.vue";
</script>

<style scoped>
.header {
  font-family: var(--font-family-admin);
  min-height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 0 var(--color-grey-60);
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
</style>
