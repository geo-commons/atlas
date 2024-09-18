<template>
  <div class="app" :style="computedStyle">
    <portal-header />
    <portal-breadcrumb />
    <router-view></router-view>
  </div>
</template>

<script>
import { useGlobalStore } from "@/stores";
import PortalHeader from "@/portal/components/PortalHeader.vue";
import PortalBreadcrumb from "@/portal/components/PortalBreadcrumb.vue";

export default {
  name: "App",
  components: {
    PortalBreadcrumb,
    PortalHeader,
  },
  compatConfig: {
    MODE: 3,
  },
  data() {
    return {
      computedStyle: { "--color-primary-organization": "#000000" },
    };
  },
  computed: {
    config() {
      return useGlobalStore().config;
    },
  },
  mounted() {
    this.computedStyle["--color-primary-organization"] = this.config.organization_primary_color;
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
@import url("https://fonts.googleapis.com/css2?family=Roboto:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap");

:root {
  /* Set default color for organization primary color. Otherwise IDE does not acknowledge its existence. */
  --color-primary-organization: #000000;

  --font-weight-light: 300;
  --font-weight-normal: 400;
  --font-weight-bold: 500;
  --font-weight-extra-bold: 700;
}

html {
  font-family: "Roboto", sans-serif;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-normal);
  line-height: 1.5;
}

.container.__portal {
  display: flex;
  flex: 1;
  flex-direction: column;
  width: 100%;
  max-width: 1280px;
  margin: 0 auto;
  font-family: var(--font-family-portal), sans-serif;
  padding-bottom: 20px;
}

.brand-color {
  color: var(--color-primary-organization);
}

h1.__portal {
  font-size: var(--font-size-2xl);
}

@media (min-width: 1024px) {
  h1.__portal {
    font-size: var(--font-size-4xl);
  }
}

.search-container {
  padding-bottom: 24px;
  width: 100%;
}

@media (min-width: 1024px) {
  .search-container {
    width: clamp(300px, 35%, 400px);
  }
}

.card-container {
  display: grid;
  grid-template-columns: repeat(auto-fit, 280px);
  row-gap: 24px;
  column-gap: 32px;
  justify-items: start;
}

@media (max-width: 660px) {
  .card-container {
    grid-template-columns: 1fr;
  }
}
</style>
