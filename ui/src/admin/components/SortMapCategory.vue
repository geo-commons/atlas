<script setup lang="ts">
import { computed, ref } from "vue";
import { useSortable } from "@dnd-kit/vue/sortable";
import DragIcon from "@/assets/icons/drag.svg";

type CategoryId = number | string;

interface MapCategoryRowItem {
  category: CategoryId;
}

interface CategoryRowProps {
  category: MapCategoryRowItem;
  index: number;
  group?: string;
  parentCategoryId?: CategoryId;
  showDragHandle: boolean;
}

const props = withDefaults(defineProps<CategoryRowProps>(), {
  group: "map-categories",
});

const rowRef = ref<HTMLElement | null>(null);
const handleRef = ref<HTMLElement | null>(null);

const sortableId = computed(() => `${props.group}-${props.category.category}`);
const sortableIndex = computed(() => props.index);
const sortableGroup = computed(() => props.group);
const sortableType = computed(() => {
  if (props.parentCategoryId === undefined) {
    return "category";
  }

  return `subcategory:${props.parentCategoryId}`;
});
const sortableData = computed(() => ({
  type: props.parentCategoryId === undefined ? "category" : "subcategory",
  categoryId: props.parentCategoryId,
}));

const { isDragging, isDropTarget } = useSortable({
  id: sortableId,
  index: sortableIndex,
  element: rowRef,
  handle: handleRef,
  group: sortableGroup,
  type: sortableType,
  accept: sortableType,
  data: sortableData,
});
</script>

<template>
  <div
    ref="rowRef"
    class="category-row tw-flex tw-touch-none tw-items-center tw-gap-2 tw-rounded-md"
    :class="{
      'tw-opacity-[0.55]': isDragging,
      'tw-shadow-[inset_0_0_0_2px_var(--color-admin-primary)]': isDropTarget,
      'tw-bg-[var(--color-admin-primary-hover)]': isDropTarget,
    }"
  >
    <button
      v-if="showDragHandle"
      ref="handleRef"
      type="button"
      class="drag-handle tw-border-0 tw-bg-transparent tw-p-2 tw-cursor-grab active:tw-cursor-grabbing"
      aria-label="Sorteer categorie"
    >
      <DragIcon class="tw-h-full tw-w-auto tw-opacity-50" aria-hidden="true" />
    </button>
    <slot />
  </div>
</template>
