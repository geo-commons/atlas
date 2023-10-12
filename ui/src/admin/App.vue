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

/* todo: check if this is the right place to set background-color.*/
body {
  background-color: var(--color-backdrop);
}

input,
button {
  margin: 0;
  padding: 0;
  border: none;
  color: inherit;
  background: transparent;
  font: inherit;
  letter-spacing: inherit;
  text-align: left;
}

input::placeholder {
  color: var(--color-text-grey);
}

button:not([disabled]) {
  cursor: pointer;
}

ul {
  margin: 0;
  padding: 0;
  list-style-type: none;
}

svg {
  flex-shrink: 0;
}

.iconbutton {
  color: black;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: border-radius 0.1s;
}

.iconbutton[disabled] {
  color: var(--color-grey-60);
}

.iconbutton.isActive {
  color: var(--color-primary);
}

.iconbutton:not([disabled]):hover {
  background: var(--color-grey-40);
}

.iconbutton:not([disabled]):active {
  background: var(--color-grey-50);
}

.iconbutton.__normal {
  width: 40px;
  height: 40px;
}

.iconbutton.__outline {
  border-radius: var(--radius-normal);
  border: 2px solid var(--color-grey-60);
}

.button:before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.button {
  position: relative;
  display: flex;
  align-items: center;
  justify-content: center;
  height: 40px;
  padding: 0 20px;
  border-radius: var(--radius-normal);
  line-height: 1;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-bold);
  text-decoration: none;
  overflow: hidden;
}

.button.__primary {
  background: var(--color-primary);
  color: white;
}

.button.__secondary {
  background: white;
  border: 2px solid var(--color-primary);
  color: var(--color-primary);
}

.button.__tertiary {
  background: white;
  border: 2px solid var(--color-grey-60);
  color: black;
}

.button.__alert {
  background: white;
  border: 2px solid var(--color-alert);
  color: var(--color-alert);
}

.button.__large {
  height: 56px;
  font-size: var(--font-size-large);
  border-width: 2px;
}

.button svg {
  margin-right: 6px;
}

.button:hover:before {
  background: var(--color-hover);
}

.button:active:before {
  background: var(--color-active);
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
