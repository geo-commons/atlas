<template>
  <header
    class="tw-bg-white tw-border tw-border-solid tw-border-gray-200 tw-border-0 tw-border-b tw-relative tw-sticky tw-top-0 tw-z-50"
  >
    <div class="tw-mx-auto tw-px-6 tw-py-4 tw-flex tw-items-center tw-justify-between">
      <div class="tw-flex tw-items-center tw-gap-6">
        <a
          href="#main-content"
          class="tw-absolute tw-sr-only focus:tw-not-sr-only tw-text-[var(--color-primary-organization)] tw-px-4 tw-py-2 tw-bg-transparent"
        >
          Ga direct naar inhoud
        </a>
        <a
          href="/"
          class="tw-flex tw-items-center tw-gap-3 hover:tw-opacity-80 tw-transition-opacity tw-no-underline focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-[var(--color-primary-organization)] focus-visible:tw-ring-offset-2 focus-visible:tw-rounded-lg"
        >
          <img
            v-if="globalStore.config?.organization_logo"
            :src="globalStore.config?.organization_logo ?? ''"
            class="tw-h-9"
            :alt="`Logo van ${globalStore.config?.organization_name}`"
          />
          <span
            v-if="globalStore.config?.organization_name && !globalStore.config?.organization_logo"
            class="tw-text-gray-700 tw-font-medium"
            >{{ globalStore.config.organization_name }}</span
          >
        </a>
        <!-- Mobile menu button -->
        <button
          type="button"
          class="tw-flex md:tw-hidden tw-items-center tw-justify-center tw-w-10 tw-h-10 tw-rounded-lg tw-text-gray-600 hover:tw-bg-gray-100 hover:tw-text-[var(--color-primary-organization)] tw-transition-colors focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-[var(--color-primary-organization)] focus-visible:tw-ring-offset-2"
          :aria-expanded="mobileMenuOpen"
          aria-label="Menu openen"
          @click="toggleMobileMenu"
        >
          <i class="pi pi-bars tw-text-xl" aria-hidden="true"></i>
        </button>
      </div>
      <!-- Desktop nav -->
      <nav class="tw-hidden md:tw-flex tw-items-center tw-gap-1" aria-label="Snel naar">
        <a
          v-for="link in visibleNavLinks"
          :key="link.href"
          :href="link.href"
          :target="link.external ? '_blank' : undefined"
          :rel="link.external ? 'noopener noreferrer' : undefined"
          :class="[
            'tw-flex tw-items-center tw-gap-2 tw-px-3 tw-py-2 tw-rounded-lg tw-transition-colors tw-text-sm tw-font-medium tw-no-underline focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-[var(--color-primary-organization)] focus-visible:tw-ring-offset-2',
            isLinkActive(link)
              ? 'tw-bg-gray-100 tw-text-[var(--color-primary-organization)]'
              : 'tw-text-gray-600 hover:tw-bg-gray-100 hover:tw-text-[var(--color-primary-organization)]',
          ]"
        >
          <i :class="['pi', link.icon, 'tw-text-base']" aria-hidden="true"></i>
          <span>{{ link.label }}</span>
        </a>
      </nav>
      <div class="tw-flex tw-items-center tw-gap-2">
        <div v-if="globalStore.user" class="tw-flex tw-items-center">
          <UserMenu current-page="portaal" />
        </div>
        <a
          v-else
          :href="`/atlas/login?next=${encodeURIComponent(nextUrl)}`"
          class="tw-flex tw-items-center tw-gap-2 tw-px-5 tw-py-2.5 tw-rounded-lg tw-border tw-border-[var(--color-primary-organization)] hover:tw-bg-[var(--color-primary-organization)] hover:tw-text-white tw-text-[var(--color-primary-organization)] tw-transition-colors tw-font-medium tw-no-underline focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-[var(--color-primary-organization)] focus-visible:tw-ring-offset-2"
        >
          <i class="pi pi-sign-in tw-text-base" aria-hidden="true"></i>
          <span>Inloggen</span>
        </a>
      </div>
    </div>
    <!-- Mobile expandable menu -->
    <Transition name="mobile-menu">
      <nav
        v-show="mobileMenuOpen"
        class="tw-absolute tw-left-0 tw-right-0 tw-top-full tw-z-50 tw-bg-white tw-border-b tw-border-gray-200 tw-shadow-lg md:tw-hidden"
        aria-label="Navigatie menu"
      >
        <ul class="tw-py-2 tw-px-4 tw-space-y-1">
          <li v-for="link in visibleNavLinks" :key="link.href">
            <a
              :href="link.href"
              :target="link.external ? '_blank' : undefined"
              :rel="link.external ? 'noopener noreferrer' : undefined"
              :class="[
                'tw-group tw-flex tw-items-center tw-gap-3 tw-w-full tw-px-4 tw-py-3 tw-rounded-lg tw-transition-colors tw-text-base tw-font-medium tw-no-underline focus-visible:tw-outline-none focus-visible:tw-ring-2 focus-visible:tw-ring-[var(--color-primary-organization)] focus-visible:tw-ring-offset-2',
                isLinkActive(link)
                  ? 'tw-bg-gray-100 tw-text-[var(--color-primary-organization)]'
                  : 'tw-text-gray-600 hover:tw-bg-gray-100 hover:tw-text-[var(--color-primary-organization)]',
              ]"
              @click="closeMobileMenu"
            >
              <i :class="['pi', link.icon, 'tw-text-lg']" aria-hidden="true"></i>
              <span>{{ link.label }}</span>
              <span
                v-if="link.external"
                class="tw-transition-opacity tw-opacity-0 group-hover:tw-opacity-100 tw-ml-1"
                style="display: inline-flex; align-items: center"
              >
                <i class="pi pi-external-link" aria-label="Externe link" />
              </span>
            </a>
          </li>
        </ul>
      </nav>
    </Transition>
  </header>
</template>

<script setup lang="ts">
import { ref, computed } from "vue";
import { useRoute } from "@/utils/inertia-routing";
import { useGlobalStore, DEFAULT_PORTAL_AVAILABLE_LINKS } from "@/stores";
import UserMenu from "@/components/UserMenu.vue";
import { PORTAL_QUICK_NAV_LINKS, type PortalQuickNavLink } from "./shared/portalQuickNavigationLinks";
import { isPortalLinkActive } from "./shared/portalUtils";

defineOptions({ name: "HeaderPortal" });

const route = useRoute();
const globalStore = useGlobalStore();

const mobileMenuOpen = ref(false);

const isLinkActive = (link: PortalQuickNavLink): boolean => isPortalLinkActive(route?.path, link);

const toggleMobileMenu = (): void => {
  mobileMenuOpen.value = !mobileMenuOpen.value;
};

const closeMobileMenu = (): void => {
  mobileMenuOpen.value = false;
};

const nextUrl = computed<string>(() =>
  typeof window !== "undefined" ? window.location.pathname + window.location.search + window.location.hash : "/",
);

const visibleNavLinks = computed<PortalQuickNavLink[]>(() => {
  const links = globalStore.portalAvailableLinks ?? DEFAULT_PORTAL_AVAILABLE_LINKS;
  return PORTAL_QUICK_NAV_LINKS.filter((link) => {
    if (link.showKey === null) return true;
    return links[link.showKey];
  });
});
</script>

<style scoped>
.mobile-menu-enter-active,
.mobile-menu-leave-active {
  transition:
    opacity 0.2s ease,
    transform 0.2s ease;
}
.mobile-menu-enter-from,
.mobile-menu-leave-to {
  opacity: 0;
  transform: translateY(-8px);
}
</style>
