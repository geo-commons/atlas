<template>
  <div class="map-container">
    <div ref="mapContainer" class="renderer-container"></div>
    <div class="bottom-right-panels">
      <div class="zoom-panel">
        <button
          v-tippy="{ placement: 'left' }"
          class="iconbutton"
          content="Zoom in"
          aria-label="Zoom in"
          @click="zoomIn"
        >
          <svg
            width="10px"
            height="10px"
            viewBox="0 0 10 10"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
          >
            <g id="Symbols" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
              <polygon id="Path" fill="#000000" points="4 10 6 10 6 6 10 6 10 4 6 4 6 0 4 0 4 4 0 4 0 6 4 6"></polygon>
            </g>
          </svg>
        </button>
        <button
          v-tippy="{ placement: 'left' }"
          class="iconbutton"
          content="Zoom uit"
          aria-label="Zoom uit"
          @click="zoomOut"
        >
          <svg
            width="10px"
            height="2px"
            viewBox="0 0 10 2"
            version="1.1"
            xmlns="http://www.w3.org/2000/svg"
            xmlns:xlink="http://www.w3.org/1999/xlink"
          >
            <g id="Symbols" stroke="none" stroke-width="1" fill="none" fill-rule="evenodd">
              <polygon id="Path" fill="#000000" points="10 2 10 0 0 0 0 2"></polygon>
            </g>
          </svg>
        </button>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from "vue";
import { register } from "ol/proj/proj4";
import Projection from "ol/proj/Projection";
import { getDefinitions } from "../../utils/projections";
import Map from "ol/Map";
import View from "ol/View";
import { Vector as VectorSource, WMTS } from "ol/source";
import { optionsFromCapabilities } from "ol/source/WMTS";
import WMTSCapabilities from "ol/format/WMTSCapabilities";
import { Tile as TileLayer, Vector as VectorLayer } from "ol/layer";
import { Point, Polygon } from "ol/geom";
import { Draw, Select, Modify, Snap } from "ol/interaction";
import Feature from "ol/Feature";
import { Style, Stroke, Fill, Circle as CircleStyle } from "ol/style";
import { defaults as defaultControls } from "ol/control";

// Register EPSG:28992 projection
register(getDefinitions());

const rdProjection = new Projection({
  code: "EPSG:28992",
  units: "m",
});

const props = defineProps<{
  layers?: any[];
  zoom?: number;
  center?: [number, number];
  onMapReady?: () => void;
}>();

const mapContainer = ref<HTMLDivElement | null>(null);
const mapRef = ref<Map | null>(null);

const olLayers: Record<string, any> = {};
const sources: Record<string, any> = {};

const drawStyle = new Style({
  image: new CircleStyle({
    radius: 7,
    fill: new Fill({ color: "#ffcc33" }),
    stroke: new Stroke({ color: "#ffcc33", width: 2 }),
  }),
});

const selectStyle = new Style({
  image: new CircleStyle({
    radius: 10,
    fill: new Fill({ color: "#2196f3" }),
    stroke: new Stroke({ color: "#fff", width: 3 }),
  }),
});

const addInteraction = (name: string, options: any) => {
  switch (name) {
    case "select": {
      const selectInteraction = new Select({ layers: [olLayers[options.layer]], style: selectStyle });
      mapRef.value?.addInteraction(selectInteraction);
      return selectInteraction;
    }
    case "snap": {
      console.log(sources[options.source]);
      const snapInteraction = new Snap({ source: sources[options.source] });
      mapRef.value?.addInteraction(snapInteraction);
      return snapInteraction;
    }
    case "draw": {
      const drawInteraction = new Draw({
        source: sources[options.source],
        type: options.type,
        style: drawStyle,
      });
      mapRef.value?.addInteraction(drawInteraction);
      return drawInteraction;
    }
    case "modify": {
      const modifyInteraction = new Modify({
        source: sources[options.source],
      });
      mapRef.value?.addInteraction(modifyInteraction);
      return modifyInteraction;
    }
    default:
      console.error("invalid interaction specified", name);
      break;
  }
};

defineExpose({ addInteraction });

function zoomIn() {
  if (mapRef.value) {
    const view = mapRef.value.getView();
    const maxZoom = view.getMaxZoom();
    const currentZoom = view.getZoom();
    if (typeof currentZoom === "number" && currentZoom < maxZoom) {
      view.animate({ zoom: currentZoom + 1, duration: 250 });
    }
  }
}

function zoomOut() {
  if (mapRef.value) {
    const view = mapRef.value.getView();
    const minZoom = view.getMinZoom();
    const currentZoom = view.getZoom();
    if (typeof currentZoom === "number" && currentZoom > minZoom) {
      view.animate({ zoom: currentZoom - 1, duration: 250 });
    }
  }
}

onMounted(async () => {
  for (const layer of props.layers ?? []) {
    if (layer.type === "wmts") {
      // Fetch WMTS capabilities and create WMTS layer
      const response = await fetch(layer.options.url);
      const body = await response.text();
      const caps = new WMTSCapabilities().read(body);
      const options = optionsFromCapabilities(caps, {
        layer: layer.options.name,
        matrixSet: "EPSG:28992",
        projection: rdProjection,
        format: "image/png",
        crossOrigin: "anonymous",
        style: "default",
      });
      if (options) {
        olLayers[layer.options.name] = new TileLayer({ source: new WMTS(options) });
      }
    } else if (layer.type === "vector") {
      const features = (layer.options.features ?? [])
        .map((f: any) => {
          if (f.type === "Point") {
            return new Feature({ geometry: new Point(f.coordinates) });
          } else if (f.type === "Polygon") {
            return new Feature({ geometry: new Polygon(f.coordinates) });
          }
          return null;
        })
        .filter(Boolean);
      const vectorSource = new VectorSource({ features });
      sources[layer.options.name] = vectorSource;
      olLayers[layer.options.name] = new VectorLayer({ source: vectorSource });
    }
  }
  const response = await fetch(`https://tiles.zaanstad.nl/mapproxy/service?REQUEST=GetCapabilities&service=wmts`);
  const body = await response.text();
  const caps = new WMTSCapabilities().read(body);
  const options = optionsFromCapabilities(caps, {
    layer: "referentiekaart",
    matrixSet: "EPSG:28992",
    projection: rdProjection,
    format: "image/png",
    crossOrigin: "anonymous",
    style: "default",
  });

  if (!options) {
    return;
  }

  const map = new Map({
    target: mapContainer.value as HTMLDivElement,
    layers: Object.values(olLayers),
    view: new View({
      center: props.center,
      zoom: props.zoom,
      projection: rdProjection,
    }),
    controls: defaultControls({
      zoom: false,
      rotate: false,
      attribution: false,
    }),
  });

  mapRef.value = map;
  if (props.onMapReady) {
    props.onMapReady();
  }
});
</script>

<style>
@import "../../assets/styles/main.css";
</style>

<style scoped>
.map-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.renderer-container {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
}

.bottom-right-panels {
  position: absolute;
  z-index: 1;
  bottom: 20px;
  right: 20px;
  display: flex;
}

.zoom-panel {
  display: flex;
  flex-direction: column;
  background: #fff;
  border-radius: var(--radius-normal);
  box-shadow: var(--shadow-normal);
  overflow: hidden;
}

.iconbutton {
  width: var(--width-button-normal);
  height: var(--width-button-normal);
}

.iconbutton:not(:last-child) {
  box-sizing: content-box;
  border-bottom: 1px solid var(--color-grey-50);
}
</style>
