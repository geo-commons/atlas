<template>
  <div v-if="false"></div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onUnmounted, inject } from "vue";
import TileLayer from "ol/layer/Tile";
import Projection from "ol/proj/Projection";
import WMTSCapabilities from "ol/format/WMTSCapabilities";
import WMTSSource, { optionsFromCapabilities } from "ol/source/WMTS";
import { useCompareLayers } from "@/composables/useCompareLayers";
import { useMapStore } from "@/stores/map_store";
import Map from "ol/Map";

interface OlWmtsLayerProps {
  id: string;
  mapId: string;
  name: string;
  url: string;
  isVisible: boolean;
  opacity: number;
  serverStyle?: string;
  zIndex: number;
  format: string;
  minZoom?: number;
  maxZoom?: number;
}

const { id, mapId, name, url, isVisible, opacity, serverStyle, zIndex, format, minZoom, maxZoom } =
  defineProps<OlWmtsLayerProps>();

const map = inject("map") as Map;
const mapStore = useMapStore(mapId);

const rdProjection = new Projection({
  code: "EPSG:28992",
  units: "m",
});

const setupSwipeEffect = ref<null | (() => void)>(null);
const handlePrerender = ref<null | ((event: any) => void)>(null);
const handlePostrender = ref<null | ((event: any) => void)>(null);
const compareLayerSettings = ref<{ active: boolean; id: string | null }>({ active: false, id: null });

let tileLayer: TileLayer<any> | null = null;

const setSource = async () => {
  const response = await fetch(`${url}?REQUEST=GetCapabilities&service=wmts`);
  const body = await response.text();
  const caps = new WMTSCapabilities().read(body);

  const options = optionsFromCapabilities(caps, {
    layer: name,
    matrixSet: "EPSG:28992",
    projection: rdProjection,
    format: format,
    crossOrigin: "anonymous",
    style: serverStyle || null,
  });

  if (!options) {
    return;
  }

  const wmtsSource = new WMTSSource(options);

  // Wait for the first tile to load before attaching swipe
  wmtsSource.on("tileloadend", () => {
    if (!compareLayerSettings.value.active) return;

    setupSwipeEffect.value?.();
    map.render();
  });

  tileLayer?.setSource(wmtsSource);
};

onMounted(() => {
  // Create tile layer with undefined source initially
  tileLayer = new TileLayer({
    visible: isVisible,
    opacity: opacity,
    zIndex: zIndex,
    source: undefined,
    minZoom: minZoom ? minZoom - 1 : undefined,
    maxZoom: maxZoom ? maxZoom : undefined,
  });

  map.addLayer(tileLayer);

  // Initialize compare layer handlers (prerender/postrender)
  const compareLayers = useCompareLayers(map, mapStore, tileLayer, id);
  setupSwipeEffect.value = compareLayers.setupSwipeEffect;
  handlePrerender.value = compareLayers.handlePrerender;
  handlePostrender.value = compareLayers.handlePostrender;

  // Set source if visible
  if (isVisible) {
    setSource();
  }
});

onUnmounted(() => {
  if (tileLayer) {
    map.removeLayer(tileLayer);
  }

  tileLayer?.un("prerender", handlePrerender.value!);
  tileLayer?.un("postrender", handlePostrender.value!);
});

watch(
  () => url,
  (value) => {
    if (tileLayer?.getSource()) {
      tileLayer.getSource().set("url", value);
    }
  },
);

watch(
  () => name,
  (value) => {
    tileLayer?.set("name", value);
  },
);

watch(
  () => isVisible,
  (value) => {
    tileLayer?.set("visible", value);

    if (value && !tileLayer?.getSource()) {
      setSource();
    }
  },
);

watch(
  () => opacity,
  (value) => {
    tileLayer?.set("opacity", value);
  },
);

// --- Watch compare layer selection
watch(
  () => [mapStore.leftSelectedCompareLayerId],
  (value, oldValue) => {
    if (mapStore.leftSelectedCompareLayerId === id && !compareLayerSettings.value.active) {
      compareLayerSettings.value = { active: true, id: mapStore.leftSelectedCompareLayerId };
      setupSwipeEffect.value?.();
      map.render();
      return;
    }

    if (
      compareLayerSettings.value.active &&
      compareLayerSettings.value.id === id &&
      mapStore.rightSelectedCompareLayerId !== id &&
      (!mapStore.leftSelectedCompareLayerId || value !== oldValue)
    ) {
      compareLayerSettings.value = { active: false, id: null };
      tileLayer?.un("prerender", handlePrerender.value!);
      tileLayer?.un("postrender", handlePostrender.value!);
      map.render();
    }
  },
);

watch(
  () => [mapStore.rightSelectedCompareLayerId],
  (value, oldValue) => {
    if (mapStore.rightSelectedCompareLayerId === id && !compareLayerSettings.value.active) {
      compareLayerSettings.value = { active: true, id: mapStore.rightSelectedCompareLayerId };
      setupSwipeEffect.value?.();
      map.render();
      return;
    }

    if (
      compareLayerSettings.value.active &&
      compareLayerSettings.value.id === id &&
      mapStore.leftSelectedCompareLayerId !== id &&
      (!mapStore.rightSelectedCompareLayerId || value !== oldValue)
    ) {
      compareLayerSettings.value = { active: false, id: null };
      tileLayer?.un("prerender", handlePrerender.value!);
      tileLayer?.un("postrender", handlePostrender.value!);
      map.render();
    }
  },
);

watch(
  () => mapStore.comparePercentage,
  () => {
    if (compareLayerSettings.value.active) {
      map.render();
    }
  },
);
</script>

<style scoped></style>
