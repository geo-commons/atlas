<template>
  <div v-if="user" class="user-menu">
    <Button
      type="button"
      :label="user.name"
      icon="pi pi-chevron-down"
      icon-pos="right"
      aria-haspopup="true"
      aria-controls="overlay_menu"
      variant="text"
      :class="[props.currentPage === 'beheer' ? '!tw-text-white' : '!tw-text-black', '!tw-bg-transparent']"
      @click="toggle"
    />
    <Menu id="overlay_menu" ref="menu" :model="menuItems" :popup="true" class="user-menu-popup">
      <template #item="{ item, props: itemProps }">
        <a
          v-if="!item.separator"
          v-bind="itemProps.action"
          :href="item.url"
          :class="item.class"
          @click="(e: Event) => handleMenuClick(e, item)"
        >
          <i :class="item.icon"></i>
          <span class="ml-2">{{ item.label }}</span>
        </a>
      </template>
    </Menu>
  </div>
</template>

<script setup lang="ts">
import "primeicons/primeicons.css";
import { ref, computed } from "vue";
import Cookies from "js-cookie";
import { useGlobalStore } from "@/stores";
import type { MenuItem as PrimeMenuItem } from "primevue/menuitem";

type CurrentPage = "portaal" | "mapviewer" | "beheer" | null;

interface MenuItem extends PrimeMenuItem {
  class?: string;
  url?: string;
}

interface UserMenuProps {
  currentPage?: CurrentPage;
}

const props = withDefaults(defineProps<UserMenuProps>(), {
  currentPage: null,
});

const menu = ref<{ toggle: (event: Event) => void } | null>(null);
const { user, config } = useGlobalStore();
const nextUrl = computed<string>(() => window.location.pathname);
const csrfToken = computed<string>(() => Cookies.get("csrftoken") || "");

const menuItems = computed(() => {
  const items: MenuItem[] = [];

  if (config?.features.portal) {
    items.push({
      label: "Portaal",
      icon: "pi pi-home",
      url: "/",
    });
  }

  items.push({
    label: "Hoofdkaart",
    icon: "pi pi-map",
    url: "/atlas/",
  });

  if (user?.is_superuser) {
    items.push({
      label: "Beheer",
      icon: "pi pi-cog",
      url: "/atlas/admin/",
    });
  }

  items.push({
    separator: true,
  });

  items.push({
    label: "Uitloggen",
    icon: "pi pi-sign-out",
    url: `/atlas/logout?next=${encodeURIComponent(nextUrl.value)}`,
  });

  return items;
});

const toggle = (event: Event): void => {
  menu.value?.toggle(event);
};

const handleMenuClick = (e: Event, item: MenuItem): void => {
  // Handle logout with POST and CSRF token (required by Django)
  if (item.url && item.url.includes("/atlas/logout")) {
    e.preventDefault();

    const form = document.createElement("form");
    form.method = "POST";
    form.action = item.url;

    // Add CSRF token to form
    const csrfInput = document.createElement("input");
    csrfInput.type = "hidden";
    csrfInput.name = "csrfmiddlewaretoken";
    csrfInput.value = csrfToken.value;
    form.appendChild(csrfInput);

    document.body.appendChild(form);
    form.submit();
    // Form will be removed when page navigates away after logout
  }
};
</script>
