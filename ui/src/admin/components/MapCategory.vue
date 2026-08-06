<template>
  <div
    class="tw-bg-white tw-px-4 tw-py-4 tw-rounded-md tw-border-solid tw-border-[var(--color-grey-60)] tw-border-[1px] tw-flex tw-flex-col tw-gap-4 tw-w-full"
  >
    <button
      type="button"
      class="tw-flex tw-items-center tw-justify-between tw-bg-transparent tw-gap-2 tw-border-0 tw-p-0 tw-cursor-pointer"
      @click="toggleOpen"
    >
      <i
        class="pi pi-chevron-down tw-text-gray-400 tw-transition-transform tw-duration-300"
        :class="{ 'tw-rotate-180': isOpen }"
      />
      <label class="tw-text-gray-400 tw-font-bold tw-cursor-pointer tw-text-[14px] tw-uppercase">
        {{ category.title }}
      </label>
    </button>

    <Transition name="expand">
      <div v-show="isOpen" class="tw-flex tw-flex-col tw-gap-2 tw-overflow-hidden">
        <slot />
      </div>
    </Transition>
  </div>
</template>

<script setup lang="ts">
const props = withDefaults(
  defineProps<{
    category: {
      id: string;
      title: string;
    };
    isOpen?: boolean;
  }>(),
  {
    isOpen: true,
  },
);

const emit = defineEmits<{
  (e: "toggle-open", categoryId: string, isOpen: boolean): void;
}>();

const toggleOpen = (): void => {
  emit("toggle-open", props.category.id, !props.isOpen);
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
