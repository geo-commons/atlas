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
<style src="vue-multiselect/dist/vue-multiselect.css" />
<style>
@import "../assets/styles/main.css";

@import url("https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,500;1,300;1,500&display=swap");

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
  align-items: center;
  font-weight: var(--font-weight-bold);
  border-top: 1px solid var(--color-grey-60);
}

.setting:last-child {
  border-bottom: 1px solid var(--color-grey-60);
}

.setting:hover {
  background: var(--color-admin-primary-hover);
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

.admin .multiselect__tags-wrap .multiselect__tag {
  background: var(--color-white);
  border: solid 1px var(--color-admin-primary);
  color: var(--color-admin-primary);
}

.admin .multiselect__tags-wrap .multiselect__tag-icon:focus,
.admin .multiselect__tags-wrap .multiselect__tag-icon:hover {
  background: var(--color-admin-primary);
}

.admin .multiselect__option--highlight {
  background: var(--color-admin-primary);
}

.admin .multiselect__tags-wrap .multiselect__tag-icon:after {
  color: var(--color-primary);
  font-size: var(--font-size-large);
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
