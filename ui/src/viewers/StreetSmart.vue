<template>
  <div ref="viewer" class="street-smart"></div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from "vue";
import { useMapStore } from "@/stores/map_store";

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
  (e: "position-changed", position: any): void;
}>();

const mapStore = useMapStore(props.mapId);

const viewer = ref<HTMLDivElement | null>(null);
const streetSmartClient = ref<any>(null);

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

    const orientation = streetSmartClient.value?.getOrientation();

    if (streetSmartClient.value) {
      streetSmartClient.value.openByCoordinate([value.marker[0], value.marker[1]]).then(() => {
        streetSmartClient.value.setOrientation(orientation);
      });
    }
  },
);

const getXYCoordinates = (xyz: [number, number, number]): [number, number] => {
  return [xyz[0], xyz[1]];
};

const initializeStreetSmartClient = () => {
  const options = {
    targetElement: viewer.value,
    username: props.username,
    password: props.password,
    apiKey: props.apiKey,
    srs: "EPSG:28992",
    locale: "nl",
  };

  window.StreetSmartApi.init(options)
    .then(() => {
      openStreetSmartClient();
    })
    .catch((err: any) => {
      console.error("Failed to initialize StreetSmart API: ", err);
    });
};

const openStreetSmartClient = () => {
  const options = {
    viewerType: [window.StreetSmartApi.ViewerType.PANORAMA],
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

  window.StreetSmartApi.open({ coordinate: [position[0], position[1], 5.6], ...options })
    .then((results) => {
      if (!results || results.length === 0) {
        return;
      }

      if (!streetSmartClient.value) {
        streetSmartClient.value = results[0];
        streetSmartClient.value.toggle3DCursor(false);
        streetSmartClient.value.setOrientation({ yaw: 0, pitch: 0 });
      }

      streetSmartClient.value.on("VIEW_CHANGE", (event) => {
        mapStore.setCycloView(event);
        const recording = streetSmartClient.value.getRecording();
        const coordinates = getXYCoordinates(recording.xyz);
        emit("position-changed", { ...props.position, marker: coordinates, source: "streetsmart" });
      });

      streetSmartClient.value.on("RECORDING_CLICK", (event) => {
        const coordinates = getXYCoordinates(event.detail.recording.xyz);
        emit("position-changed", { ...props.position, marker: coordinates, source: "streetsmart" });
      });
    })
    .catch((err: any) => {
      console.error("Failed to open StreetSmart viewer: ", err);
    });
};

onMounted(() => {
  initializeStreetSmartClient();
});

onBeforeUnmount(() => {
  window.StreetSmartApi.destroy({
    targetElement: viewer.value,
  });

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
