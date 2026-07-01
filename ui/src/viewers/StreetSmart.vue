<template>
  <div ref="viewer" class="street-smart"></div>
</template>

<script setup lang="ts">
import { PanoramaViewerEvents, StreetSmartApi, ViewerType, type PanoramaViewer } from "@cyclomedia/streetsmart-api";
import { ref, watch, onMounted, onBeforeUnmount } from "vue";
import { useMapStore } from "@/stores/map_store";
import { vec3 } from "gl-matrix";

interface Position {
  marker: [number, number];
  source: string;
}

interface StreetSmartProps {
  position: Position;
  username: string;
  password: string;
  apiKey: string;
  mapId: string;
}

const props = defineProps<StreetSmartProps>();

const emit = defineEmits<{
  (e: "position-changed", position: Position): void;
}>();

const mapStore = useMapStore(props.mapId);

const viewer = ref<HTMLDivElement | null>(null);
const streetSmartClient = ref<PanoramaViewer | null>(null);

watch(
  () => props.position,
  (value, prevValue) => {
    if (value.source === "streetsmart") {
      return;
    }

    if (!value?.marker) {
      return;
    }

    if (
      value.marker &&
      prevValue?.marker &&
      value.marker[0] === prevValue.marker[0] &&
      value.marker[1] === prevValue.marker[1]
    ) {
      return;
    }

    const client = streetSmartClient.value;

    if (!client) {
      return;
    }

    const orientation = client.getOrientation();

    client.openByCoordinate([value.marker[0], value.marker[1], 5.6], "EPSG:28992").then(() => {
      client.setOrientation(orientation);
    });
  },
);

const getXYCoordinates = (xyz: vec3): [number, number] => {
  return [xyz[0], xyz[1]];
};

const initializeStreetSmartClient = async () => {
  if (!viewer.value) {
    return;
  }

  const options = {
    targetElement: viewer.value,
    username: props.username,
    password: props.password,
    apiKey: props.apiKey,
    loginOauth: false,
    srs: "EPSG:28992",
    locale: "nl",
  } as const;

  try {
    await StreetSmartApi.init(options);
    await openStreetSmartClient();
  } catch (err) {
    console.error("Failed to initialize StreetSmart API: ", err);
  }
};

const openStreetSmartClient = async () => {
  const options = {
    viewerType: [ViewerType.PANORAMA],
    srs: "EPSG:28992",
    panoramaViewer: {
      closable: false,
      maximizable: false,
      pitch: 0,
    },
    obliqueViewer: {
      closable: false,
      maximizable: false,
    },
  };
  const position = props.position.marker;

  try {
    const results = await StreetSmartApi.open({ coordinate: [position[0], position[1], 5.6] }, options);

    if (!results || results.length === 0) {
      return;
    }

    if (!streetSmartClient.value) {
      streetSmartClient.value = results[0] as PanoramaViewer;
      streetSmartClient.value.toggle3DCursor(false);
      streetSmartClient.value.setOrientation({ yaw: 0, pitch: 0 });
    }

    const client = streetSmartClient.value;

    client.on(PanoramaViewerEvents.VIEW_CHANGE, (event) => {
      mapStore.setCycloView(event);
      const recording = client.getRecording();
      const coordinates = getXYCoordinates(recording.xyz);
      emit("position-changed", { ...props.position, marker: coordinates, source: "streetsmart" });
    });

    client.on(PanoramaViewerEvents.RECORDING_CLICK, (event) => {
      const coordinates = getXYCoordinates(event.detail.recording.xyz);
      emit("position-changed", { ...props.position, marker: coordinates, source: "streetsmart" });
    });
  } catch (err) {
    console.error("Failed to open StreetSmart viewer: ", err);
  }
};

onMounted(() => {
  initializeStreetSmartClient();
});

onBeforeUnmount(() => {
  if (viewer.value) {
    StreetSmartApi.destroy({
      targetElement: viewer.value,
      loginOauth: false,
    });
  }

  mapStore.setCycloView(null);
});
</script>

<style scoped>
.street-smart {
  width: 100%;
  height: 100%;
  padding-top: 32px; /* make sure buttons of Atlas do not overlap buttons of StreetSmart */
}
</style>
