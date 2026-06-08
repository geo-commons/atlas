<script setup lang="ts">
import { computed, ref } from "vue";
import { useSortable } from "@dnd-kit/vue/sortable";
import DragIcon from "@/assets/icons/drag.svg";

type LayerId = number | string;
type CategoryId = number | string;

interface LayerCategory {
  id: CategoryId;
}

interface MapLayerRowItem {
  id: LayerId;
  category?: LayerCategory | null;
}

interface LayerRowProps {
  layer: MapLayerRowItem;
  index: number;
  group: string;
  categoryId: CategoryId;
  parentCategoryId?: CategoryId;
  showDragHandle: boolean;
}

const props = defineProps<LayerRowProps>();

const rowRef = ref<HTMLElement | null>(null);
const handleRef = ref<HTMLElement | null>(null);

const sortableId = computed(() => `${props.group}-${props.layer.id}`);
const sortableIndex = computed(() => props.index);
const sortableGroup = computed(() => props.group);
const sortableType = computed(() => `layer:${props.categoryId}`);
const sortableData = computed(() => ({
  type: props.parentCategoryId === undefined ? "category-layer" : "subcategory-layer",
  categoryId: props.categoryId,
  parentCategoryId: props.parentCategoryId,
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
    class="layer-row tw-flex tw-w-full tw-touch-none tw-items-center tw-gap-2 tw-rounded-md"
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
      aria-label="Sorteer laag"
    >
      <DragIcon class="tw-h-full tw-w-auto tw-opacity-50" aria-hidden="true" />
    </button>
    <slot />
  </div>
</template>
