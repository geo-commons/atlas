<template>
  <div
    class="tw-flex tw-flex-row tw-justify-between tw-bg-white tw-px-4 tw-py-2 tw-rounded-md tw-border-solid tw-border-[var(--color-grey-60)] tw-border-[1px]"
  >
    <button
      v-if="openLayerSettings"
      type="button"
      class="tw-bg-white tw-flex tw-items-center tw-gap-2"
      @click="openLayerSettings(getLayerId(layer))"
    >
      <span class="tw-font-bold">
        {{ layer.title }}
      </span>
      <ViewIcon v-if="isLayerVisible" v-tippy content="Standaard zichtbaar" class="icon __smedium reset-transform" />
    </button>
    <div v-else class="tw-bg-white tw-flex tw-items-center tw-gap-2">
      <span class="tw-font-bold">
        {{ layer.title }}
      </span>
    </div>
    <div v-if="!isChangingOrder">
      <Button icon="pi pi-ellipsis-h" aria-label="Save" variant="text" severity="contrast" @click="toggleMenu" />
      <Menu ref="menu" :model="items" popup />
    </div>
  </div>
</template>

<script setup lang="ts">
import { ILayer } from "@/types/layer";
import { ref } from "vue";
import Menu from "primevue/menu";
import ViewIcon from "@/assets/icons/view-icon.svg";

import type { MenuItem } from "primevue/menuitem";

type MapLayerItemLayer = Omit<ILayer, "id"> & { id: number | string; internal_id?: number | string };

const props = withDefaults(
  defineProps<{
    layer: MapLayerItemLayer;
    openLayerSettings?: (layerId: number | string) => void;
    isLayerVisible: boolean;
    deselectLayer?: (layer: ILayer) => void;
    selectLayer?: (layer: ILayer) => void;
    isChangingOrder?: boolean;
  }>(),
  { isChangingOrder: false },
);

const { layer, openLayerSettings, isLayerVisible, deselectLayer, selectLayer, isChangingOrder } = props;

const getLayerId = (layer: MapLayerItemLayer): number | string => {
  return layer.internal_id ?? layer.id;
};

const menu = ref<InstanceType<typeof Menu> | null>(null);

const items: MenuItem[] = [
  ...(openLayerSettings
    ? [
        {
          label: "Bewerk instellingen",
          command: () => openLayerSettings?.(getLayerId(layer)),
        },
      ]
    : []),

  ...(deselectLayer
    ? [
        {
          label: "Deselecteer laag",
          command: () => deselectLayer?.(layer),
        },
      ]
    : []),

  ...(selectLayer
    ? [
        {
          label: "Selecteer laag",
          command: () => selectLayer?.(layer),
        },
      ]
    : []),
];

const toggleMenu = (event: Event) => {
  menu.value?.toggle(event);
};
</script>
