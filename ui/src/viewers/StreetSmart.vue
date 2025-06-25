<template>
  <div ref="viewer" class="street-smart"></div>
</template>

<script setup lang="ts">
import { ref, watch, onMounted, onBeforeUnmount } from "vue";
import { useMapStore } from "@/stores/map_store";

interface Position {
  marker: [number, number];
}

interface StreetSmartProps {
  position: Position;
  username: string;
  password: string;
  apiKey: string;
  mapId: string;
}

const props = defineProps<StreetSmartProps>();

const mapStore = useMapStore(props.mapId);

const viewer = ref<HTMLDivElement | null>(null);

watch(
  () => props.position,
  (value, prevValue) => {
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

    setPosition(value.marker);
  },
);

const setPosition = (position: [number, number]) => {
  const options = {
    viewerType: [window.StreetSmartApi.ViewerType.PANORAMA],
    panoramaViewer: {
      closable: false,
      maximizable: false,
    },
    obliqueViewer: {
      closable: false,
      maximizable: false,
    },
  };

  window.StreetSmartApi.open(`${position[0]}, ${position[1]}`, options)
    .then((results) => {
      if (!results || results.length === 0) {
        return;
      }

      const viewerInstance = results[0];
      viewerInstance.toggle3DCursor(false);

      viewerInstance.on("VIEW_CHANGE", (event) => {
        mapStore.setCycloView(event);
      });
    })
    .catch((err: any) => {
      console.error("Failed to open StreetSmart viewer: ", err);
    });
};

onMounted(() => {
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
      setPosition(props.position.marker);
    })
    .catch((err: any) => {
      console.error("Failed to initialize StreetSmart API: ", err);
    });
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
