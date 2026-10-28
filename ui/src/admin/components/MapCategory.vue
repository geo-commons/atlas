<template>
  <div
    class="tw-bg-white tw-px-4 tw-pt-2 tw-rounded-md tw-border-solid tw-border-[var(--color-grey-60)] tw-border-[1px] tw-flex tw-flex-col tw-gap-4 tw-w-full"
    :class="isOpen ? 'tw-pb-4' : 'tw-pb-2'"
  >
    <div class="tw-flex tw-items-center tw-justify-between tw-gap-2">
      <button
        type="button"
        class="tw-flex tw-items-center tw-bg-transparent tw-gap-2 tw-border-0 tw-p-0 tw-cursor-pointer"
        :aria-label="`${isOpen ? 'Inklappen' : 'Uitklappen'}: ${category.title}`"
        @click="toggleOpen"
      >
        <i
          class="pi pi-chevron-down tw-text-gray-400 tw-transition-transform tw-duration-300"
          :class="{ 'tw-rotate-180': isOpen }"
        />
      </button>
      <label
        class="tw-flex-1 tw-text-gray-400 tw-font-bold tw-cursor-pointer tw-text-[14px] tw-uppercase"
        @click="toggleOpen"
      >
        {{ category.title }}
      </label>
      <div v-if="editable">
        <Button
          icon="pi pi-ellipsis-h"
          :aria-label="`Meer opties voor ${category.title}`"
          variant="text"
          severity="contrast"
          @click="toggleMenu"
        />
        <Menu ref="menu" :model="items" popup />
      </div>
    </div>

    <Transition name="expand">
      <div v-show="isOpen" class="tw-flex tw-flex-col tw-gap-2 tw-overflow-hidden">
        <slot />
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
import { ref } from "vue";
import Menu from "primevue/menu";

import type { MenuItem } from "primevue/menuitem";

const props = withDefaults(
  defineProps<{
    category: {
      id: string;
      title: string;
    };
    isOpen?: boolean;
    editable?: boolean;
  }>(),
  {
    isOpen: true,
    editable: false,
  },
);

const emit = defineEmits<{
  (e: "toggle-open", categoryId: string, isOpen: boolean): void;
  (e: "edit-title", categoryId: string, title: string): void;
}>();

const menu = ref<InstanceType<typeof Menu> | null>(null);

const items: MenuItem[] = [
  {
    label: "Naam bewerken",
    command: () => emit("edit-title", props.category.id, props.category.title),
  },
];

const toggleOpen = (): void => {
  emit("toggle-open", props.category.id, !props.isOpen);
};

const toggleMenu = (event: Event): void => {
  menu.value?.toggle(event);
};
</script>

<style scoped>
.expand-enter-active,
.expand-leave-active {
  transition:
    max-height 0.25s ease,
    opacity 0.2s ease;
  max-height: 600px;
  opacity: 1;
}

.expand-enter-from,
.expand-leave-to {
  max-height: 0;
  opacity: 0;
}
</style>
