<template>
  <div class="app" data-testid="app">
    <header-menu v-if="!isEmbed && config.features.portal" />
    <map-renderer
      v-if="readyToRenderMap"
      ref="map"
      :initial-position="position"
      :initial-layers="layers"
      :user="user"
      :features="map.features"
      :settings="map.settings"
      :config="config"
      :is-embed="isEmbed"
      :map-id="map.is_main ? 'primary' : map.slug || 'primary'"
    />
  </div>
</template>

<script>
import Cookies from "js-cookie";
import HeaderMenu from "../components/HeaderMenu";
import MapRenderer from "../components/MapRenderer/MapRenderer";
import { mapState, mapStores } from "pinia";
import { useGlobalStore } from "@/stores";
import "primeicons/primeicons.css";

export default {
  name: "App",
  components: {
    HeaderMenu,
    MapRenderer,
  },
  data() {
    return {
      readyToRenderMap: false,
    };
  },
  computed: {
    ...mapState(useGlobalStore, ["position", "layers", "config", "map", "user", "isEmbed"]),
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
        this.readyToRenderMap = true;
        return false;
      }

      const data = await response.json();

      this.globalStore.setUser({ ...this.user, token: data.token });

      this.readyToRenderMap = true;
    },
  },
};
</script>

<style>
@import "../assets/styles/main.css";
</style>

<style scoped>
.app {
  display: flex;
  flex-direction: column;
  width: 100%;
  height: 100%;
}
</style>
