<template>
  <li class="sublayer">
    <input
      :id="layer.id"
      type="checkbox"
      :name="layer.id"
      :checked="layer.is_visible"
      :disabled="isDisabled"
      @click="onSelect"
    />
    <label :for="layer.id">
      {{ layer.title }}
    </label>
    <LayerAuthentication v-if="layer.login_required && (!user || !user.token)" />
    <button
      v-if="layer.zoom_min && position.zoom < layer.zoom_min"
      v-tippy="{ placement: 'right' }"
      class="zoom-button"
      content="Zoom in om deze laag te bekijken"
      aria-label="Zoom in om deze laag te bekijken"
      @click="(e) => zoomIn(e)"
    >
      <ZoomInIcon />
    </button>
    <button
      v-if="layer.zoom_max && position.zoom > layer.zoom_max"
      v-tippy="{ placement: 'right' }"
      class="zoom-button"
      content="Zoom uit om deze laag te bekijken"
      aria-label="Zoom uit om deze laag te bekijken"
      @click="(e) => zoomOut(e)"
    >
      <ZoomOutIcon />
    </button>
    <LayerFit v-if="layer.extent" :layer="layer" @click="onFit" />
    <LayerInfo :layer="layer" />
  </li>
</template>

<script setup lang="ts">
import { computed } from "vue";
import { intersects } from "ol/extent";
import LayerAuthentication from "@/components/LayerAuthentication.vue";
import LayerFit from "@/components/LayerFit.vue";
import LayerInfo from "@/components/LayerInfo.vue";
import ZoomInIcon from "@/assets/icons/zoom-in-icon.svg";
import ZoomOutIcon from "@/assets/icons/zoom-out-icon.svg";
import { IPosition } from "@/types/map";
import { ILayer } from "@/types/layer";
import { IUser } from "@/types/user";
import { useMapStore } from "@/stores/map_store";

interface LayerListItemProps {
  layer: ILayer;
  position: IPosition;
  user: IUser | null;
  mapId: string;
}

const props = defineProps<LayerListItemProps>();

const emit = defineEmits<{
  (e: "set-position", position: IPosition): void;
  (e: "on-fit", extent: number[]): void;
}>();

const mapStore = useMapStore(props.mapId);

const isDisabled = computed(() => {
  if (props.layer.login_required && (!props.user || !props.user.token)) {
    return true;
  }

  if (props.layer.zoom_min && props.position.zoom < props.layer.zoom_min) {
    return true;
  }

  if (props.layer.zoom_max && props.position.zoom > props.layer.zoom_max) {
    return true;
  }

  if (props.layer.extent && props.position.extent && !intersects(props.layer.extent, props.position.extent)) {
    return true;
  }

  return false;
});

const onSelect = () => {
  if (isDisabled.value) {
    return;
  }

  mapStore.toggleLayer({
    selectedLayerId: props.layer.id,
    is_visible: !props.layer.is_visible,
  });
};

const onFit = () => {
  if (props.layer.extent) {
    emit("on-fit", props.layer.extent);
  }
};

const zoomIn = (e: MouseEvent) => {
  e.stopPropagation();

  if (props.layer.zoom_min) {
    emit("set-position", {
      ...props.position,
      zoom: props.layer.zoom_min,
    });
  }

  if (!props.layer.is_visible) {
    mapStore.toggleLayer({ selectedLayerId: props.layer.id, is_visible: true });
  }
};

const zoomOut = (e: MouseEvent) => {
  e.stopPropagation();

  if (props.layer.zoom_max) {
    emit("set-position", {
      ...props.position,
      zoom: props.layer.zoom_max,
    });
  }

  if (!props.layer.is_visible) {
    mapStore.toggleLayer({ selectedLayerId: props.layer.id, is_visible: true });
  }
};
</script>

<style scoped>
.sublayer {
  position: relative;
  display: flex;
}

.sublayer > input {
  position: absolute;
  top: 5px;
  left: 0;
  width: 14px;
  height: 14px;
  margin: 0;
}

.sublayer > label {
  display: flex;
  position: relative;
  width: 100%;
  cursor: pointer;
  padding: 2px 0 2px 20px;
  user-select: none;
  word-break: break-word;
}

.sublayer > input:disabled + label {
  color: var(--color-grey-80);
}

.zoom-button {
  margin-left: 5px;
  opacity: 0;
}

.sublayer:hover .zoom-button,
.tippy-active > .zoom-button,
.keyboard-user .zoom-button:focus {
  opacity: 1;
}
</style>
