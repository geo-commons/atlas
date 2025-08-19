<template>
  <div class="header container tw-bg-indigo-600">
    <router-link to="/" class="dashboard-title">
      <MenuIcon class="icon __white" />
      Atlas beheer
    </router-link>

    <Button
      type="button"
      :label="user?.name"
      icon="pi pi-chevron-down"
      icon-pos="right"
      aria-haspopup="true"
      aria-controls="overlay_menu"
      variant="text"
      severity="primary"
      @click="toggle"
    />
    <Menu id="overlay_menu" ref="menu" :model="items" :popup="true">
      <template #item="{ item, props }">
        <a v-bind="props.action" :href="item.url" @click.prevent="handleMenuClick(item)">
          <i :class="item.icon"></i>
          <span class="ml-2">{{ item.label }}</span>
        </a>
      </template>
    </Menu>
  </div>
</template>

<script setup lang="ts">
import Cookies from "js-cookie";
import { useGlobalStore } from "@/stores";
import { storeToRefs } from "pinia";
import { ref, Ref } from "vue";
import MenuIcon from "../../assets/icons/menu-icon.svg";

interface MenuItem {
  label: string;
  icon: string;
  url: string;
}

interface User {
  name: string;
}

interface MenuRef {
  toggle: (event: Event) => void;
}

const menu = ref<MenuRef | null>(null);
const items = ref<MenuItem[]>([
  {
    label: "Uitloggen",
    icon: "pi pi-sign-out",
    url: "/atlas/logout",
  },
]);

const globalStore = useGlobalStore();
const { user } = storeToRefs(globalStore) as { user: Ref<User | null> };

const toggle = (event: Event): void => {
  menu.value?.toggle(event);
};

const csrfToken = Cookies.get("csrftoken") || "";
function handleMenuClick(item: MenuItem) {
  if (item.url === "/atlas/logout") {
    const form = document.createElement("form");
    form.method = "POST";
    form.action = `/atlas/logout`;

    const csrfInput = document.createElement("input");
    csrfInput.type = "hidden";
    csrfInput.name = "csrfmiddlewaretoken";
    csrfInput.value = csrfToken;
    form.appendChild(csrfInput);

    document.body.appendChild(form);
    form.submit();
  } else {
    window.location.href = item.url;
  }
}
</script>

<style scoped>
.header {
  font-family: var(--font-family-admin);
  min-height: 56px;
  display: flex;
  align-items: center;
  justify-content: space-between;
  box-shadow: 0 1px 0 var(--color-grey-60);
}

.dashboard-title {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-left: 8px;
  color: var(--color-white);
  font-weight: var(--font-weight-bold);
  font-size: var(--font-size-xl);
  text-decoration: none;
}

.header .p-button.p-button-text.p-button-primary {
  background-color: transparent;
  color: var(--color-white);
}

.header .p-button.p-button-text.p-button-primary:hover {
  background-color: transparent;
}
</style>
