<template>
  <div class="indicator-container container" :class="environmentStyle">
    <div class="environment-wrapper"><MediumWarningIcon />Let op: dit is de {{ applicationEnvironment }}!</div>
  </div>
</template>

<script>
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";
import MediumWarningIcon from "../../assets/icons/medium-warning-icon.svg";

export default {
  name: "AdminEnvironmentIndicator",
  components: { MediumWarningIcon },
  computed: {
    ...mapState(useGlobalStore, ["config"]),
    applicationEnvironment() {
      if (this.config.application_environment === "development") {
        return "ontwikkelomgeving";
      }

      return "acceptatieomgeving";
    },
    environmentStyle() {
      if (this.config.application_environment === "development") {
        return "development-colour-scheme";
      }

      return "acceptation-colour-scheme";
    },
  },
};
</script>

<style scoped>
.indicator-container {
  font-family: var(--font-family-admin);
  display: flex;
  min-height: 40px;
  align-items: center;
  justify-content: space-between;
}

.environment-wrapper {
  display: flex;
  align-items: center;
  gap: 4px;
  margin-left: 8px;
  font-size: var(--font-size-normal);
  font-weight: var(--font-weight-bold);
  text-decoration: none;
}

.development-colour-scheme {
  color: #1a56db;
  background-color: #c3ddfd;
}

.acceptation-colour-scheme {
  color: #cc5500;
  background-color: #f2d5be;
}
</style>
