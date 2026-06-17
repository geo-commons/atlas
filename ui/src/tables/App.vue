<template>
  <div class="app">
    <header-menu v-if="config.features.portal" />
    <slot />
  </div>
</template>

<script>
import HeaderMenu from "../components/HeaderMenu";
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";

export default {
  name: "App",
  components: {
    HeaderMenu,
  },
  computed: {
    ...mapState(useGlobalStore, ["config"]),
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

html {
  font-family: var(--font-family);
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
</style>
