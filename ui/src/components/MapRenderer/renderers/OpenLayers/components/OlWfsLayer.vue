<template>
  <div v-if="false"></div>
</template>

<script setup>
import { inject, onMounted, onUnmounted, toRaw, watch } from "vue";
import VectorLayer from "ol/layer/Vector";
import { bbox as bboxStrategy } from "ol/loadingstrategy";
import GeoJSON from "ol/format/GeoJSON";
import VectorSource from "ol/source/Vector";
import { Circle, Fill, Stroke, Style } from "ol/style";
import OpenLayersParser from "geostyler-openlayers-parser";
import { useMapStore } from "@/stores/map_store";
import { getLayerFilter } from "@/utils/layer-filter-wfs";

const olParser = new OpenLayersParser();

const DEFAULT_STYLE = [
  new Style({
    stroke: new Stroke({
      color: "blue",
      width: 3,
    }),
    fill: new Fill({
      color: "rgba(0, 0, 255, 0.1)",
    }),
  }),
  new Style({
    image: new Circle({
      radius: 10,
      fill: new Fill({
        color: "blue",
      }),
    }),
  }),
];

const props = defineProps({
  id: String,
  mapId: String,
  name: String,
  url: String,
  layer: String,
  isVisible: Boolean,
  isSelectable: Boolean,
  selectedFeatures: Array,
  opacity: Number,
  clientStyle: Object,
  zIndex: Number,
  minZoom: Number,
  maxZoom: Number,
});

const map = inject("map");
const mapStore = useMapStore(props.mapId);

let source;
let tileLayer;

const getStyle = async (inputStyle) => {
  if (!inputStyle || Object.keys(inputStyle).length === 0) {
    return DEFAULT_STYLE;
  }

  try {
    const olStyle = await olParser.writeStyle(toRaw(inputStyle));
    return olStyle.output;
  } catch (e) {
    console.error("Unable to parse style", props.name, e);
  }

  return DEFAULT_STYLE;
};

onMounted(async () => {
  source = new VectorSource({
    format: new GeoJSON(),
    strategy: bboxStrategy,
    url: (extent) => {
      const params = new URLSearchParams([
        ["service", "WFS"],
        ["version", "2.0.0"],
        ["request", "GetFeature"],
        ["typeNames", props.name],
        ["outputFormat", "application/json"],
        ["srsname", "EPSG:28992"],
        ["count", "5000"],
      ]);

      params.set("FILTER", getLayerFilter(mapStore.layerFilters, props.id, extent) ?? "");

      const url = new URL(props.url);
      url.search = params.toString();

      return url.toString();
    },
  });

  source.on("addfeature", ({ feature }) => {
    feature.set("layer_id", props.id, true);
  });

  tileLayer = new VectorLayer({
    id: props.id,
    name: props.name,
    visible: props.isVisible,
    source: source,
    opacity: props.opacity,
    zIndex: props.zIndex,
    selectable: props.isSelectable,
    minZoom: props.minZoom ? props.minZoom - 1 : undefined,
    maxZoom: props.maxZoom ? props.maxZoom : undefined,
  });

  map.addLayer(tileLayer);

  const style = await getStyle(
    props.clientStyle && props.clientStyle["default"] ? props.clientStyle["default"] : props.clientStyle,
  );
  tileLayer.setStyle(style);
});

onUnmounted(() => {
  map.removeLayer(tileLayer);
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
    tileLayer.setVisible(value);
  },
);

watch(
  () => props.opacity,
  (value) => {
    tileLayer.set("opacity", value);
  },
);

watch(
  () => props.clientStyle,
  async (value) => {
    const style = await getStyle(value);
    tileLayer.setStyle(style);
  },
);

watch(
  () => mapStore.layerFilters,
  () => {
    source.refresh();
  },
  { deep: true },
);
</script>
