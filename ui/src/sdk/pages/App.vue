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
}>();

const polygonCoords = [
  [
    [116044.06969709918, 495387.60845237196],
    [116036.42889836353, 495385.8300816352],
    [116041.44790271131, 495365.34220878844],
    [116048.77752176934, 495366.9938547696],
    [116044.06969709918, 495387.60845237196],
  ],
];

const pointOne = [116039.55578897425, 495373.06592906645];
const pointTwo = [116045.62957295871, 495380.7780762627];
const pointThree = [116040.36077535816, 495369.7799269963];

const mapContainer = ref<HTMLDivElement | null>(null);

const mapRef = ref<Map | null>(null);

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

  const polygonFeature = new Feature({
    geometry: new Polygon(polygonCoords),
  });
  polygonFeature.setStyle(
    new Style({
      stroke: new Stroke({ color: "#1976d2", width: 2 }),
      fill: new Fill({ color: "rgba(25, 118, 210, 0.2)" }),
    }),
  );
  const vectorSource = new VectorSource({ features: [polygonFeature] });
  const vectorLayer = new VectorLayer({ source: vectorSource });

  const pointsSource = new VectorSource({
    features: [
      new Feature({ geometry: new Point(pointOne) }),
      new Feature({ geometry: new Point(pointTwo) }),
      new Feature({ geometry: new Point(pointThree) }),
    ],
  });
  const pointsLayer = new VectorLayer({ source: pointsSource });

  const map = new Map({
    target: mapContainer.value as HTMLDivElement,
    layers: [
      new TileLayer({
        source: new WMTS(options),
      }),
      vectorLayer,
      pointsLayer,
    ],
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

  const polygonGeometry = polygonFeature.getGeometry();
  if (polygonGeometry) {
    map.getView().fit(polygonGeometry.getExtent(), {
      padding: [100, 100, 100, 100],
    });
  }

  const drawInteraction = new Draw({
    source: vectorSource,
    type: "Point",
    style: new Style({
      image: new CircleStyle({
        radius: 7,
        fill: new Fill({ color: "#ffcc33" }),
        stroke: new Stroke({ color: "#ffcc33", width: 2 }),
      }),
    }),
  });

  drawInteraction.on("drawend", (e) => {
    console.log(e.feature.getGeometry());
  });

  const selectInteraction = new Select({
    layers: [pointsLayer],
    style: new Style({
      image: new CircleStyle({
        radius: 10,
        fill: new Fill({ color: "#2196f3" }),
        stroke: new Stroke({ color: "#fff", width: 3 }),
      }),
    }),
  });

  const modifyInteraction = new Modify({
    source: pointsSource,
  });

  map.addInteraction(drawInteraction);
  map.addInteraction(selectInteraction);
  map.addInteraction(modifyInteraction);

  // Add snap interaction for the polygon and drawn points
  const snapInteraction = new Snap({ source: vectorSource, pixelTolerance: 15 });
  map.addInteraction(snapInteraction);
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
