<template>
  <div v-if="false"></div>
</template>

<script setup>
import { inject, onMounted, onUnmounted, toRaw, watch } from "vue";
import Select from "ol/interaction/Select";
import VectorLayer from "ol/layer/Vector";
import { bbox as bboxStrategy } from "ol/loadingstrategy";
import GeoJSON from "ol/format/GeoJSON";
import VectorSource from "ol/source/Vector";
import { Circle, Fill, Stroke, Style } from "ol/style";
import OpenLayersParser from "geostyler-openlayers-parser";
import { useMapStore } from "@/stores/map_store";

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

const emit = defineEmits(["features-selected"]);

const map = inject("map");
const mapStore = useMapStore(props.mapId);

let source;
let tileLayer;
let select;

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

const onSelectFeatures = (e) => {
  const features = e.target.getFeatures().getArray();
  if (features.length === 0) {
    return;
  }

  emit("features-selected", features);
};

onMounted(async () => {
  source = new VectorSource({
    format: new GeoJSON(),
    strategy: bboxStrategy,
    url: (extent) => {
      const params = new URLSearchParams([
        ["service", "WFS"],
        ["version", "1.0.0"],
        ["request", "GetFeature"],
        ["typename", props.name],
        ["outputFormat", "application/json"],
        ["srsname", "EPSG:28992"],
        ["bbox", extent.join(",")],
      ]);

      const url = new URL(props.url);
      url.search = params.toString();

      return url.toString();
    },
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

  if (props.isSelectable) {
    const activeStyle = await getStyle(
      props.clientStyle && props.clientStyle["active"] ? props.clientStyle["active"] : props.clientStyle,
    );

    select = new Select({
      layers: [tileLayer],
      style: activeStyle,
    });

    select.on("select", onSelectFeatures);
    map.addInteraction(select);
  }
});

onUnmounted(() => {
  if (select) {
    map.removeInteraction(select);
  }
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
  () => props.clientStyle,
  async (value) => {
    const style = await getStyle(value);
    tileLayer.setStyle(style);
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
        const filterValues = value[props.id][key][filterKey];
        const values = filterValues
          .filter((filterValue) => filterValue !== "Leeg")
          .map((filterValue) => `'${filterValue}'`)
          .join(",");

        let valueFilters = [];
        if (filterValues.includes("Leeg")) {
          valueFilters.push(`(${filterKey} IS NULL or ${filterKey} = '')`);
        }

        // Check to make sure filterKey has values
        if (values.length > 0) {
          valueFilters.push(`${filterKey} IN (${values})`);
        }

        if (valueFilters.length > 0) {
          cqlFilters.push(`(${valueFilters.join(" OR ")})`);
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
  () => props.selectedFeatures,
  (features) => {
    if (select && features && features.length === 0) {
      select.getFeatures().clear();
    }
  },
  { deep: true },
);
</script>
