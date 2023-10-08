<template>
  <div class="app">
    <header-menu />
    <router-view></router-view>
  </div>
</template>

<script>
import HeaderMenu from "../components/HeaderMenu.vue";

export default {
  name: "App",
  components: {
    HeaderMenu,
  },
};
</script>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}
</style>

<style>
@import "../assets/styles/main.css";
:root {
  --color-text-grey: rgba(0, 0, 0, 0.55);

  --color-grey-20: #eaeaea; /* divider (list items, files) */
  --color-grey-30: #dddddd; /* divider (sections, header) */
  --color-grey-40: #f5f5f5;
  --color-grey-50: #eaeaea;
  --color-grey-60: #dadada;
  --color-grey-80: #949494;

  --color-icon-grey: rgba(0, 0, 0, 0.42);

  --color-tooltip-dark: #222222;

  --color-alert: #eb0000;

  --color-hover: rgba(0, 0, 0, 0.03);
  --color-active: rgba(0, 0, 0, 0.06);

  --font-size-tiny: 12px;
  --font-size-small: 14px;
  --font-size-normal: 16px;
  --font-size-large: 18px;

  --font-weight-normal: 300;
  --font-weight-bold: 500;

  --radius-small: 4px;
  --radius-normal: 8px;

  --shadow-normal: 0 0 1px rgba(0, 0, 0, 0.2), 0 0 8px rgba(0, 0, 0, 0.15);

  --padding-screen: 8px;

  --width-detail: 100vw;
  --width-button-small: 24px;
  --width-button-normal: 32px;
  --width-button-large: 40px;
}

@media (min-width: 576px) {
  :root {
    --width-detail: 300px;
    --padding-screen: 16px;
  }
}

@media (min-width: 768px) {
  :root {
    --width-detail: 350px;
  }
}

@media (min-width: 1200px) {
  :root {
    --width-detail: 400px;
    --padding-screen: 20px;
  }
}

@import url("https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,500;1,300;1,500&display=swap");

html {
  font-family: "Roboto", sans-serif;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-normal);
  line-height: 1.5;
}

*,
*:after,
*:before {
  box-sizing: border-box;
}

/* Remove outline from all focused elements */
*:focus {
  outline: none;
  outline-offset: -2px;
}

/* Remove highlight color on Android */
* {
  -webkit-tap-highlight-color: rgba(0, 0, 0, 0);
}

html.keyboard-user *:focus {
  outline: 2px solid var(--color-primary);
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
</style>
