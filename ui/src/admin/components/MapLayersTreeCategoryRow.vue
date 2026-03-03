<script setup lang="ts">
import { computed, ref } from "vue";
import { type IDragEvent, makeDraggable, makeDroppable } from "@vue-dnd-kit/core";
import DragIcon from "@/assets/icons/drag.svg";

type CategoryId = number | string;

interface MapCategoryRowItem {
  category: CategoryId;
}

interface CategoryDragMeta {
  categoryId: CategoryId;
}

interface CategoryReorderPayload {
  fromIndex: number;
  toIndex: number;
}

interface CategoryRowProps {
  category: MapCategoryRowItem;
  index: number;
  categories: MapCategoryRowItem[];
  isTarget?: boolean;
}

type CategoryDragPayload = [number, MapCategoryRowItem[], CategoryDragMeta];
type CategoryDropzonePayload = [MapCategoryRowItem[], CategoryDragMeta];
type CategoryDndEvent = IDragEvent<MapCategoryRowItem, CategoryDragMeta, MapCategoryRowItem, CategoryDragMeta>;

const props = withDefaults(defineProps<CategoryRowProps>(), {
  isTarget: false,
});

const emit = defineEmits<{
  (e: "reorder", payload: CategoryReorderPayload): void;
  (e: "drag-start", payload: { index: number; categoryId: CategoryId }): void;
  (e: "drag-hover", payload: { index: number; categoryId: CategoryId }): void;
  (e: "drag-end"): void;
}>();

const rowRef = ref<HTMLElement | null>(null);

const payload = (): CategoryDragPayload => [props.index, props.categories, { categoryId: props.category.category }];

const { isDragging, isDragOver } = makeDraggable(
  rowRef,
  {
    groups: ["map-categories"],
    dragHandle: ".drag-handle",
    events: {
      onSelfDragStart() {
        emit("drag-start", { index: props.index, categoryId: props.category.category });
      },
      onSelfDragEnd() {
        emit("drag-end");
      },
      onSelfDragCancel() {
        emit("drag-end");
      },
      onHover() {
        emit("drag-hover", { index: props.index, categoryId: props.category.category });
      },
    },
  },
  payload,
);

makeDroppable(
  rowRef,
  {
    groups: ["map-categories"],
    events: {
      // @ts-expect-error niet nodig
      onDrop(event: CategoryDndEvent) {
        const fromIndex = Number(event.payload?.index);
        if (!Number.isInteger(fromIndex)) {
          return;
        }

        emit("reorder", {
          fromIndex,
          toIndex: props.index,
        });
      },
    },
  },
  (): CategoryDropzonePayload => [props.categories, { categoryId: props.category.category }],
);

const isDropTarget = computed(
  () => props.isTarget || Boolean(isDragOver.value?.center || isDragOver.value?.top || isDragOver.value?.bottom),
);
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
      type="button"
      class="drag-handle tw-border-0 tw-bg-transparent tw-p-2 tw-cursor-grab active:tw-cursor-grabbing"
      aria-label="Sorteer categorie"
    >
      <DragIcon class="tw-h-full tw-w-auto tw-opacity-50" aria-hidden="true" />
    </button>
    <slot />
  </div>
</template>
