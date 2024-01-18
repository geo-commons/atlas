<template>
  <div class="app">
    <AppMenu v-if="$route.meta.menu" />
    <router-view></router-view>
  </div>
</template>

<script>
import AppMenu from "./components/MainMenu.vue";

export default {
  name: "App",
  components: {
    AppMenu,
  },
};
</script>

<!-- Include multiselect -->
<style src="vue-multiselect/dist/vue-multiselect.min.css" />
<style>
@import "../assets/styles/main.css";

@import url("https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,500;1,300;1,500&display=swap");

html {
  font-family: "Roboto", sans-serif;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-normal);
  line-height: 1.5;
}

body {
  background-color: var(--color-backdrop);
}

select {
  padding: 0 16px;
  border: 1px solid var(--color-grey-60);
  border-radius: var(--radius-normal);
  font-family: "Roboto", sans-serif;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-normal);
}

.container.__admin {
  display: flex;
  flex-direction: column;
  justify-content: center;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
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

.sidebar {
  flex-shrink: 0;
  position: relative;
  width: var(--width-detail);
  z-index: 1;
  box-shadow: var(--shadow-normal);
}

.sidebar h1 {
  height: 40px;
  margin: 0;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-bold);

  display: flex;
  align-items: center;
  justify-content: center;
}

.sidebar h1 svg {
  margin-right: 6px;
}

.sidebar h2 {
  margin: 24px 0 8px;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-bold);
}

.settings {
  margin: 0 calc(var(--padding-screen) * -1);
}

.setting {
  width: 100%;
  height: 41px;
  padding: 0 8px 0 16px;
  display: flex;
  align-items: center;
  font-weight: var(--font-weight-bold);
  border-top: 1px solid var(--color-grey-60);
}

.setting:last-child {
  border-bottom: 1px solid var(--color-grey-60);
}

.setting:hover {
  background: var(--color-primary-hover);
}

input[type="text"],
input[type="number"],
input[type="email"],
input[type="url"] {
  width: 100%;
  border: 1px solid var(--color-grey-60);
  border-radius: var(--radius-normal);
  padding: 0 16px;
  height: 40px;
}

input[type="checkbox"] {
  padding: 0 16px;
  margin-right: 5px;
}

input:disabled {
  background: var(--color-grey-40);
}

.edit-field-border {
  border-radius: var(--radius-normal);
  border: 1px solid var(--color-grey-60);
}

.button.__secondary:not([disabled]):hover {
  background: var(--color-primary-hover);
}

.multiselect__tags > input {
  border: none;
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
  background-color: var(--color-primary-hover);
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
