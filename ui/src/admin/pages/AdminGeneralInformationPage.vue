<template>
  <div class="container __admin">
    <div class="top-menu-container">
      <div class="page-title-wrapper no-padding">
        <h1>Algemene gegevens</h1>
      </div>
    </div>

    <ul class="details-wrapper">
      <li v-if="config.organization_name" class="detail-wrapper">
        <div class="detail-label">
          <OrganizationIcon class="icon" />
          Organisatie
        </div>
        <div>
          {{ config.organization_name }}
        </div>
      </li>
      <li v-if="config.application_version" class="detail-wrapper">
        <div class="detail-label">
          <TagIcon class="icon" />
          Versie
        </div>
        <div>
          {{ config.application_version }}
        </div>
      </li>
      <li v-if="config.application_environment" class="detail-wrapper">
        <div class="detail-label">
          <DatabaseIcon class="icon" />
          Omgeving
        </div>
        <div>
          {{ applicationEnvironment }}
        </div>
      </li>
    </ul>
  </div>
</template>

<script>
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";
import OrganizationIcon from "../../assets/icons/organization-icon.svg";
import TagIcon from "../../assets/icons/tag-icon.svg";
import DatabaseIcon from "@/assets/icons/database-icon.svg";

export default {
  name: "AdminGeneralInformationPage",
  components: {
    DatabaseIcon,
    OrganizationIcon,
    TagIcon,
  },
  computed: {
    ...mapState(useGlobalStore, ["config"]),
    applicationEnvironment() {
      switch (this.config.application_environment) {
        case "development":
          return "Ontwikkel";
        case "production":
          return "Productie";
      }
      return "Acceptatie";
    },
  },
};
</script>

<style>
.details-wrapper {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.detail-wrapper {
  display: flex;
  flex-direction: column;
  gap: 4px;
  font-size: var(--font-size-large);
}

.detail-label {
  display: flex;
  gap: 4px;
  align-items: center;
  font-weight: var(--font-weight-bold);
}
</style>
