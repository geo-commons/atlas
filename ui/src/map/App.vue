<template>
  <div class="app">
    <header-menu v-if="config.features.portal" />
    <map-renderer
      ref="map"
      :initial-position="position"
      :initial-layers="visibleLayers"
      :user="user"
      :features="map.features"
      :settings="map.settings"
      @position-changed="positionChanged"
    />
  </div>
</template>

<script>
import { mapState } from "vuex";
import HeaderMenu from "../components/HeaderMenu";
import MapRenderer from "../components/MapRenderer/MapRenderer";

export default {
  name: "App",
  components: {
    HeaderMenu,
    MapRenderer,
  },
  data() {
    return {
      user: null,
    };
  },
  computed: {
    ...mapState({
      position: (state) => state.position,
      layers: (state) => state.layers,
      config: (state) => state.config,
      map: (state) => state.map,
    }),
    visibleLayers() {
      if (this.map.layers) {
        return this.layers
          .filter((layer) => this.map.layers.includes(layer.internal_id) || (layer.is_base && layer.is_visible))
          .map((layer) => {
            return {
              ...layer,
              is_visible: !layer.is_base ? true : layer.is_visible,
            };
          });
      }

      return this.layers;
    },
  },
  watch: {
    position(value) {
      this.showInfoPanel = Boolean(value.marker);
      this.pushHistoryState();
    },
    layers() {
      this.pushHistoryState();
    },
  },
  methods: {
    pushHistoryState() {
      const basePath = /(.*?)(@|$)/.exec(window.location.pathname);

      const x = encodeURIComponent(this.position.center[0].toFixed(2));
      const y = encodeURIComponent(this.position.center[1].toFixed(2));
      const zoom = encodeURIComponent(this.position.zoom);

      const layers = this.visibleLayers
        .filter((l) => !l.is_base)
        .map((l) => l.id)
        .join(",");

      const baseLayer = this.visibleLayers.filter((l) => l.is_base).map((l) => l.id);

      window.history.replaceState({}, "", `${basePath[1]}@${x},${y},${zoom}z/layers=${layers}/base=${baseLayer.length > 0 ? baseLayer[0] : ""}`);
    },
    positionChanged(position) {
      this.$store.commit("setPosition", position);
    },
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

.sidebar input[type="text"] {
  width: 100%;
  border: 1px solid var(--color-grey-80);
  border-radius: var(--radius-small);
  padding: 0 16px;
  height: 40px;
}

.multiselect__tags > input {
  border: none;
}

/* For some reason map/App.vue does not allow multiselect style to be overridden via main.css. */
/* Override multiselect style */
.multiselect__tag {
  background: var(--color-white);
  border: solid 1px var(--color-primary);
  color: var(--color-primary);
}

.multiselect__tag-icon:focus,
.multiselect__tag-icon:hover {
  background: var(--color-primary);
}

.multiselect__option--highlight {
  background: var(--color-primary);
}

.multiselect__placeholder {
  color: var(--color-text-grey);
}

.multiselect__tags {
  border-color: var(--color-grey-60);
  border-radius: var(--radius-normal);
}
.multiselect__tag-icon:after {
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
