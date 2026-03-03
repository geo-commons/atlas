<script setup lang="ts">
import { computed, ref } from "vue";
import { type IDragEvent, makeDraggable, makeDroppable } from "@vue-dnd-kit/core";
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

interface LayerDragMeta {
  layerId: LayerId;
  categoryId?: CategoryId;
}

interface LayerReorderPayload {
  fromIndex: number;
  toIndex: number;
  categoryId?: CategoryId;
}

interface LayerRowProps {
  layer: MapLayerRowItem;
  index: number;
  layers: MapLayerRowItem[];
  group: string;
  isTarget?: boolean;
}

type LayerDragPayload = [number, MapLayerRowItem[], LayerDragMeta];
type LayerDropzonePayload = [MapLayerRowItem[], LayerDragMeta];
type LayerDndEvent = IDragEvent<MapLayerRowItem, LayerDragMeta, MapLayerRowItem, LayerDragMeta>;

const props = withDefaults(defineProps<LayerRowProps>(), {
  isTarget: false,
});

const emit = defineEmits<{
  (e: "reorder", payload: LayerReorderPayload): void;
  (e: "drag-start", payload: { index: number; layerId: LayerId; categoryId?: CategoryId }): void;
  (e: "drag-hover", payload: { index: number; layerId: LayerId; categoryId?: CategoryId }): void;
  (e: "drag-end"): void;
}>();

const rowRef = ref<HTMLElement | null>(null);

const payload = (): LayerDragPayload => [
  props.index,
  props.layers,
  { layerId: props.layer.id, categoryId: props.layer.category?.id },
];

const { isDragging, isDragOver } = makeDraggable(
  rowRef,
  {
    groups: [props.group],
    dragHandle: ".drag-handle",
    events: {
      onSelfDragStart() {
        emit("drag-start", { index: props.index, layerId: props.layer.id, categoryId: props.layer.category?.id });
      },
      onSelfDragEnd() {
        emit("drag-end");
      },
      onSelfDragCancel() {
        emit("drag-end");
      },
      onHover() {
        emit("drag-hover", { index: props.index, layerId: props.layer.id, categoryId: props.layer.category?.id });
      },
    },
  },
  payload,
);

makeDroppable(
  rowRef,
  {
    groups: [props.group],
    events: {
      // @ts-expect-error niet nodig
      onDrop(event: LayerDndEvent) {
        const fromIndex = Number(event.payload?.index);
        if (!Number.isInteger(fromIndex)) {
          return;
        }

        emit("reorder", {
          fromIndex,
          toIndex: props.index,
          categoryId: props.layer.category?.id,
        });
      },
    },
  },
  (): LayerDropzonePayload => [props.layers, { layerId: props.layer.id, categoryId: props.layer.category?.id }],
);

const isDropTarget = computed(
  () => props.isTarget || Boolean(isDragOver.value?.center || isDragOver.value?.top || isDragOver.value?.bottom),
);
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
      type="button"
      class="drag-handle tw-border-0 tw-bg-transparent tw-p-2 tw-cursor-grab active:tw-cursor-grabbing"
      aria-label="Sorteer laag"
    >
      <DragIcon class="tw-h-full tw-w-auto tw-opacity-50" aria-hidden="true" />
    </button>
    <slot />
  </div>
</template>
