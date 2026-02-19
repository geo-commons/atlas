<template>
  <div>
    <h2 class="tw-text-2xl tw-mb-6 tw-mt-2">Direct naar</h2>
    <ul class="tw-space-y-2">
      <li v-for="link in visibleLinks" :key="link.href">
        <a
          :href="link.href"
          :target="link.external ? '_blank' : undefined"
          :rel="link.external ? 'noopener noreferrer' : undefined"
          :class="[
            'tw-w-full tw-flex tw-items-center tw-gap-3 tw-px-4 tw-py-3 tw-rounded-xl tw-transition-colors tw-group tw-text-left tw-no-underline',
            isLinkActive(link)
              ? 'tw-bg-gray-50 focus-visible:tw-bg-gray-50 focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-[var(--color-primary-organization)] focus-visible:tw-ring-offset-2'
              : 'hover:tw-bg-gray-50 focus-visible:tw-bg-gray-50 focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-[var(--color-primary-organization)] focus-visible:tw-ring-offset-2',
          ]"
        >
          <i
            :class="[
              'pi',
              link.icon,
              'tw-text-lg tw-transition-colors',
              isLinkActive(link)
                ? 'tw-text-[var(--color-primary-organization)]'
                : 'tw-text-[var(--color-text-organization)] group-hover:tw-text-[var(--color-primary-organization)]',
            ]"
            aria-hidden="true"
          ></i>
          <span
            :class="[
              'tw-font-medium',
              isLinkActive(link)
                ? 'tw-text-[var(--color-title-organization)]'
                : 'tw-text-[var(--color-text-organization)] group-hover:tw-text-[var(--color-title-organization)]',
            ]"
            >{{ link.label }}</span
          >
        </a>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { useRoute } from "vue-router";
import { useGlobalStore, DEFAULT_PORTAL_AVAILABLE_LINKS } from "@/stores";
import { PORTAL_QUICK_NAV_LINKS } from "./shared/portalQuickNavigationLinks";
import { isPortalLinkActive } from "./shared/portalUtils";
import type { PortalQuickNavLink } from "./shared/portalQuickNavigationLinks";

defineOptions({ name: "PortalQuickNavigationMenu" });

const route = useRoute();
const globalStore = useGlobalStore();
const isLinkActive = (link: PortalQuickNavLink): boolean => isPortalLinkActive(route?.path, link);

const visibleLinks = computed<PortalQuickNavLink[]>(() => {
  const links = globalStore.portalAvailableLinks ?? DEFAULT_PORTAL_AVAILABLE_LINKS;
  return PORTAL_QUICK_NAV_LINKS.filter((link) => {
    if (link.showInQuickMenu === false) return false;
    if (link.showKey === null) return true;
    return links[link.showKey];
  });
});
</script>
