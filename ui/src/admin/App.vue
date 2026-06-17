<template>
  <div class="app">
    <Toast position="bottom-center" />
    <AppMenu v-if="$route.meta.menu" />
    <AdminEnvironmentIndicator
      v-if="
        config.application_environment !== 'production' &&
        (!$route.query.admin_env_indicator || $route.query.admin_env_indicator?.toLowerCase() !== 'hide')
      "
    />
    <admin-breadcrumb v-if="$route.meta.menu" />
    <slot v-if="readyToRenderAdmin" />
  </div>
</template>

<script>
import Cookies from "js-cookie";
import AppMenu from "./components/MainMenu.vue";
import AdminBreadcrumb from "./components/AdminBreadcrumb.vue";
import AdminEnvironmentIndicator from "@/admin/components/AdminEnvironmentIndicator.vue";
import { mapState, mapStores } from "pinia";
import { useGlobalStore } from "@/stores";
import "primeicons/primeicons.css";

export default {
  name: "App",
  components: {
    AdminEnvironmentIndicator,
    AdminBreadcrumb,
    AppMenu,
  },
  data() {
    return {
      readyToRenderAdmin: false,
    };
  },
  computed: {
    ...mapState(useGlobalStore, ["config", "user"]),
    ...mapStores(useGlobalStore),
  },
  created() {
    this.fetchAccessToken();

    this.fetchInterval = setInterval(
      () => {
        this.fetchAccessToken();
      },
      1000 * 60 * 5,
    ); // every 5 minutes
  },
  unmounted() {
    clearInterval(this.fetchInterval);
  },
  methods: {
    async fetchAccessToken() {
      const response = await fetch("/atlas/api/v1/token", {
        method: "POST",
        credentials: "same-origin",
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookies.get("csrftoken"),
        },
      });

      if (!response.ok) {
        this.readyToRenderAdmin = true;
        return false;
      }

      const data = await response.json();

      this.globalStore.setUser({ ...this.user, token: data.token });

      this.readyToRenderAdmin = true;
    },
  },
};
</script>

<style>
@import "../assets/styles/main.css";
@import "vue-advanced-cropper/dist/style.css";

body {
  background-color: var(--color-backdrop);
}

select {
  padding: 0 16px;
  border: 1px solid var(--color-grey-60);
  border-radius: var(--radius-normal);
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-normal);
}

select.__admin {
  font-family: var(--font-family-admin);
}

.container.__admin {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  font-family: var(--font-family-admin);
  padding-bottom: 32px;
}

.section + .section {
  padding-top: 0;
}

.flexer {
  display: flex;
  justify-content: center;
}

.flexer > *:not(:last-child) {
  margin-right: 12px;
}

.setting {
  width: 100%;
  height: 41px;
  padding: 0 8px 0 16px;
  display: flex;
  gap: 8px;
  align-items: center;
  font-weight: 400;
  border-top: 1px solid var(--color-grey-60);
}

.setting:last-child {
  border-bottom: 1px solid var(--color-grey-60);
}

.setting:hover {
  background: var(--color-admin-primary-hover);
}

.advance-settings-wrapper {
  display: flex;
  gap: 12px;
  flex-direction: column;
}

.edit-field-border {
  border-radius: var(--radius-normal);
  border: 1px solid var(--color-grey-60);
}

.top-menu-container {
  padding: 20px 0;
  display: flex;
  flex-direction: column;
  justify-content: space-between;
}

.page-title-wrapper {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  padding-bottom: 24px;
}

.top-menu-button-container {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.advance-button-wrapper {
  display: flex;
  gap: 12px;
}

.admin-btn-wrapper {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.admin-search-wrapper {
  width: clamp(300px, 35%, 400px);
  height: 48px;
  position: relative;
}

.admin-search-wrapper svg {
  position: absolute;
  top: 0;
  bottom: 0;
  left: 16px;
  margin: auto 0;
  pointer-events: none;
}

.admin-search-wrapper input {
  width: 100%;
  height: 100%;
  padding: 0 0 0 48px;
  border: 1px solid var(--color-grey-60);
  border-radius: var(--radius-normal);
}

@media (max-width: 576px) {
  .page-title-wrapper {
    flex-direction: column;
    align-items: flex-start;
    padding-bottom: 0;
  }

  .admin-search-wrapper {
    width: 100%;
  }

  .top-menu-container {
    gap: 16px;
  }

  .top-menu-button-container {
    flex-direction: column;
    width: 100%;
  }
}

.admin-content-wrapper {
  display: flex;
  flex-direction: column;
  gap: 20px;
  padding-bottom: 40px;
}

.admin-title-link {
  text-decoration: none;
  color: var(--color-black);
}

.admin-title-link:hover {
  text-decoration: underline;
}

.admin-table {
  width: 100%;
  border-collapse: collapse;
  background: var(--color-white);
}

.admin-table > tbody > tr:hover {
  background-color: var(--color-admin-primary-hover);
}

.admin-table thead tr th {
  text-align: left;
  font-weight: var(--font-weight-normal);
  color: var(--color-text-grey);
  padding-top: 10px;
  padding-bottom: 10px;
}

.admin-table thead tr th:not(:last-child) {
  padding-right: 8px;
}

.admin-table > tbody > tr.table-border:not(:last-child) > td,
th {
  border-bottom: 1px solid var(--color-grey-60);
}

.admin-table > tbody > tr > td:not(:nth-last-child(-n + 2)) {
  padding-right: 8px;
}

.admin-table > tbody > tr > td.btn-col {
  width: 50px;
}

.first-column-padding {
  padding-left: 12px;
}
</style>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}
</style>
