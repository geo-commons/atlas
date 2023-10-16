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

@media (max-width: 575px) {
  .container {
    padding: 0 20px;
  }

  .section {
    padding: 32px 0;
  }
}

@media (min-width: 576px) {
  .container {
    padding: 0 32px;
  }

  .section {
    padding: 40px 0;
  }
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

input[type="text"],
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

.edit-field-border {
  border-radius: var(--radius-normal);
  border: 1px solid var(--color-grey-60);
}

.multiselect__tags > input {
  border: none;
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
