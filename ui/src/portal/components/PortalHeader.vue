<template>
  <header class="tw-bg-white tw-border tw-border-solid tw-border-gray-200 tw-border-0 tw-border-b">
    <div class="tw-mx-auto tw-px-6 tw-py-4 tw-flex tw-items-center tw-justify-between">
      <div class="tw-flex tw-items-center tw-gap-6">
        <a href="/" class="tw-flex tw-items-center tw-gap-3 hover:tw-opacity-80 tw-transition-opacity tw-no-underline">
          <img
            v-if="config.organization_logo"
            :src="config.organization_logo"
            class="tw-h-9"
            :alt="`Logo van ${config.organization_name}`"
          />
          <span v-if="config.organization_name" class="tw-text-gray-700 tw-font-medium">{{
            config.organization_name
          }}</span>
        </a>
      </div>
      <!-- TODO: menu toevoegen -->
      <div v-if="user" class="tw-flex tw-items-center">
        <UserMenu current-page="portaal" />
      </div>
      <a
        v-else
        :href="`/atlas/login?next=${encodeURIComponent(nextUrl)}`"
        class="tw-flex tw-items-center tw-gap-2 tw-px-5 tw-py-2.5 tw-rounded-lg tw-border tw-border-[var(--color-primary-organization)] hover:tw-bg-[var(--color-primary-organization)] hover:tw-text-white tw-text-[var(--color-primary-organization)] tw-transition-colors tw-font-medium tw-no-underline"
      >
        <i class="pi pi-sign-in tw-text-base" aria-hidden="true"></i>
        <span>Inloggen</span>
      </a>
    </div>
  </header>
</template>

<script>
import { mapState } from "pinia";
import { useGlobalStore } from "@/stores";
import UserMenu from "@/components/UserMenu.vue";

export default {
  name: "HeaderPortal",
  components: { UserMenu },
  computed: {
    ...mapState(useGlobalStore, ["user", "config"]),
    nextUrl() {
      return window.location.pathname;
    },
  },
};
</script>
