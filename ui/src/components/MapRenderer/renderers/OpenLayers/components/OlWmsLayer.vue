<template>
  <div v-if="false"></div>
</template>

<script setup>
import { inject, onMounted, onUnmounted, ref, watch } from "vue";
import Projection from "ol/proj/Projection";
import TileLayer from "ol/layer/Tile";
import TileWMSSource from "ol/source/TileWMS";
import { storeToRefs } from "pinia";
import { useGlobalStore } from "@/stores";
import { useMapStore } from "@/stores/map_store";
import { useCompareLayers } from "@/composables/useCompareLayers";

const props = defineProps({
  id: String,
  mapId: String,
  name: String,
  url: String,
  layer: String,
  isVisible: Boolean,
  sendTokenWithRequest: Boolean,
  opacity: Number,
  zIndex: Number,
  format: String,
  serverStyle: String,
  minZoom: Number,
  maxZoom: Number,
});

const map = inject("map");
const globalStore = useGlobalStore();
const mapStore = useMapStore(props.mapId);
const { user } = storeToRefs(globalStore);

const setupSwipeEffect = ref(null);
const handlePrerender = ref(null);
const handlePostrender = ref(null);
const compareLayerSettings = ref({ active: false, id: null });

const rdProjection = new Projection({
  code: "EPSG:28992",
  units: "m",
});

const authenticatedTileLoader = (token) => {
  return (tile, src) => {
    const client = new XMLHttpRequest();
    client.responseType = "blob";
    client.open("GET", src);
    client.setRequestHeader("Authorization", `Bearer ${token}`);

    client.onload = () => {
      if (client.response) {
        const objectURL = URL.createObjectURL(client.response);
        tile.getImage().onload = () => {
          URL.revokeObjectURL(objectURL);
        };
        tile.getImage().src = objectURL;
      } else {
        tile.setState(3);
      }
    };

    client.onerror = () => {
      tile.setState(3);
    };

    client.send();
  };
};

let source;
let tileLayer;

// Create source and layer
onMounted(() => {
  source = new TileWMSSource({
    url: props.url,
    crossOrigin: "anonymous",
    params: {
      VERSION: "1.1.1",
      FORMAT: props.format,
      LAYERS: props.name,
      STYLES: props.serverStyle ? props.serverStyle : "",
      tiled: true,
      tilesOrigin: 117000 + "," + 498000.00000000023,
    },
    projection: rdProjection,
    tileLoadFunction: props.sendTokenWithRequest ? authenticatedTileLoader(user.value.token) : null,
  });

  tileLayer = new TileLayer({
    id: props.id,
    name: props.name,
    visible: props.isVisible,
    opacity: props.opacity,
    source: source,
    zIndex: props.zIndex,
    minZoom: props.minZoom ? props.minZoom - 1 : undefined,
    maxZoom: props.maxZoom ? props.maxZoom : undefined,
  });

  map.addLayer(tileLayer);
  const compareLayers = useCompareLayers(map, mapStore, tileLayer, props.id);
  setupSwipeEffect.value = compareLayers.setupSwipeEffect;
  handlePrerender.value = compareLayers.handlePrerender;
  handlePostrender.value = compareLayers.handlePostrender;
});

// Clean up on unmount
onUnmounted(() => {
  map.removeLayer(tileLayer);

  // Remove event listeners
  tileLayer.un("prerender", handlePrerender.value);
  tileLayer.un("postrender", handlePostrender.value);
});

// Watch for prop changes
watch(
  () => props.url,
  (value) => {
    source.set("url", value);
  },
);

watch(
  () => props.name,
  (value) => {
    tileLayer.set("name", value);
  },
);

watch(
  () => props.isVisible,
  (value) => {
    tileLayer.set("visible", value);
  },
);

watch(
  () => props.opacity,
  (value) => {
    tileLayer.set("opacity", value);
  },
);

watch(
  () => mapStore.layerFilters,
  (value) => {
    // If filters object is empty, refresh source
    if (!Object.keys(value).length) {
      source.updateParams({
        ...source.getParams(),
        CQL_FILTER: null,
      });
      source.refresh();
      return;
    }

    // Don't filter if there are no filters specified for specific layer
    if (!Object.keys(value).includes(props.id)) {
      return;
    }

    if (!value[props.id]) {
      return;
    }

    const cqlFilters = [];

    Object.keys(value[props.id]).forEach((key) => {
      if (key === "searchQuery" && value[props.id]["searchQuery"] !== "") {
        cqlFilters.push(value[props.id][key]);
        return;
      }

      if (value[props.id][key].length == 0) {
        return;
      }

      Object.keys(value[props.id][key]).map((filterKey) => {
        const values = value[props.id][key][filterKey].map((filterValue) => `'${filterValue}'`).join(",");

        // Check to make sure filterKey has values
        if (values.length) {
          cqlFilters.push(`${filterKey} IN (${values})`);
        }
      });
    });

    source.updateParams({
      ...source.getParams(),
      CQL_FILTER: cqlFilters.length > 0 ? cqlFilters.join(" AND ") : null,
    });

    source.refresh();
  },
  { deep: true },
);

watch(
  () => [mapStore.leftSelectedCompareLayerId],
  (value, oldValue) => {
    // Check if this layer is newly selected to compare
    if (mapStore.leftSelectedCompareLayerId === props.id && !compareLayerSettings.value.active) {
      setupSwipeEffect.value();

      compareLayerSettings.value = {
        active: true,
        id: mapStore.leftSelectedCompareLayerId,
      };

      return;
    }

    // Check if there is no longer a left layer selected to compare
    if (
      compareLayerSettings.value.active &&
      compareLayerSettings.value.id === props.id &&
      mapStore.rightSelectedCompareLayerId !== props.id &&
      (!mapStore.leftSelectedCompareLayerId || value !== oldValue)
    ) {
      compareLayerSettings.value = {
        active: false,
        id: null,
      };

      tileLayer.un("prerender", handlePrerender.value);
      tileLayer.un("postrender", handlePostrender.value);
      map.render();
    }
  },
);
//
watch(
  () => [mapStore.rightSelectedCompareLayerId],
  (value, oldValue) => {
    // not active register this layer as compare layer
    if (mapStore.rightSelectedCompareLayerId === props.id && !compareLayerSettings.value.active) {
      setupSwipeEffect.value();

      compareLayerSettings.value = {
        active: true,
        id: mapStore.rightSelectedCompareLayerId,
      };

      return;
    }

    // Check if there is no longer a left layer selected to compare
    if (
      compareLayerSettings.value.active &&
      compareLayerSettings.value.id === props.id &&
      mapStore.leftSelectedCompareLayerId !== props.id &&
      (!mapStore.rightSelectedCompareLayerId || value !== oldValue)
    ) {
      compareLayerSettings.value = {
        active: false,
        id: null,
      };

      tileLayer.un("prerender", handlePrerender.value);
      tileLayer.un("postrender", handlePostrender.value);
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
