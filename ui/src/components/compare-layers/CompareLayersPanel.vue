<template>
  <Drawer
    :visible="showCompareLayerPanel"
    header="Kaartlagen vergelijken"
    position="right"
    :pt="{
      mask: '!tw-bg-black/0',
    }"
    @update:visible="closePanel"
  >
    <div class="tw-flex tw-flex-col tw-gap-4">
      <ExplainerMessage>
        <template #icon>
          <InformationCircleIcon />
        </template>
        <template #explainer>
          Kies twee kaartlagen om met elkaar te vergelijken. Gebruik vervolgens de slider onderin het scherm om de
          verschillen tussen de twee kaartlagen te bekijken."
        </template>
      </ExplainerMessage>
      <div class="tw-flex tw-flex-col tw-gap-2">
        <label for="">Selecteer een kaartlaag links</label>
        <Select
          :model-value="mapStore.leftSelectedCompareLayerId"
          :options="leftSelectableLayers"
          filter
          name="left-selectable-layers"
          option-label="title"
          option-value="id"
          placeholder="Selecteer kaartlaag"
          fluid
          :pt="{
            overlay: '!tw-max-w-48',
          }"
          @update:model-value="onSelectLeftLayer"
        />
      </div>
      <div class="tw-flex tw-flex-col tw-gap-2">
        <label for="">Selecteer een kaartlaag rechts</label>
        <Select
          :model-value="mapStore.rightSelectedCompareLayerId"
          :options="rightSelectableLayers"
          filter
          name="right-selectable-layers"
          option-label="title"
          option-value="id"
          placeholder="Selecteer kaartlaag"
          fluid
          :pt="{
            overlay: '!tw-max-w-48',
          }"
          @update:model-value="onSelectRightLayer"
        />
      </div>
    </div>

    <template #footer>
      <div class="tw-flex tw-items-center tw-gap-2">
        <Button label="Sluit" class="tw-flex-auto" outlined @click="closePanel">
          <ClosePanelIcon />
          Sluit
        </Button>
        <Button class="tw-flex-auto" @click="stopCompareLayers">
          <CompareLayersIcon class="tw-fill-white" />
          Stop vergelijken
        </Button>
      </div>
    </template>
  </Drawer>
</template>

<script setup lang="ts">
import CompareLayersIcon from "@/assets/icons/compare-layers-icon.svg";
import ClosePanelIcon from "@/assets/icons/close-panel-icon.svg";
import { ILayer } from "@/types/layer";
import { computed } from "vue";
import { useMapStore } from "@/stores/map_store";
import InformationCircleIcon from "../../assets/icons/information-circle-icon.svg";
import ExplainerMessage from "@/components/ExplainerMessage.vue";

interface CompareLayerProps {
  mapId: string;
  layers: Array<ILayer>;
  showCompareLayerPanel?: boolean;
}

// Props
const { mapId, layers, showCompareLayerPanel } = defineProps<CompareLayerProps>();

// Emits
const emit = defineEmits<{
  (e: "close-panel"): void;
  (e: "stop-compare"): void;
}>();

// Store
const mapStore = useMapStore(mapId);

const closePanel = () => {
  emit("close-panel");
};

const stopCompareLayers = () => {
  mapStore.setLeftSelectedCompareLayerId(null);
  mapStore.setRightSelectedCompareLayerId(null);
  emit("stop-compare");
};

const leftSelectableLayers = computed(() => {
  if (mapStore.rightSelectedCompareLayerId) {
    return layers.filter((l) => l.id !== mapStore.rightSelectedCompareLayerId);
  }

  return layers;
});

const rightSelectableLayers = computed(() => {
  if (mapStore.leftSelectedCompareLayerId) {
    return layers.filter((l) => l.id !== mapStore.leftSelectedCompareLayerId);
  }

  return layers;
});

const onSelectLeftLayer = (layerId: string) => {
  if (mapStore.leftSelectedCompareLayerId !== null) {
    mapStore.toggleLayer({ selectedLayerId: mapStore.leftSelectedCompareLayerId, is_visible: false });
  }

  mapStore.setLeftSelectedCompareLayerId(layerId);
  mapStore.toggleLayer({ selectedLayerId: layerId, is_visible: true });
};

const onSelectRightLayer = (layerId: string) => {
  if (mapStore.rightSelectedCompareLayerId !== null) {
    mapStore.toggleLayer({ selectedLayerId: mapStore.rightSelectedCompareLayerId, is_visible: false });
  }

  mapStore.setRightSelectedCompareLayerId(layerId);
  mapStore.toggleLayer({ selectedLayerId: layerId, is_visible: true });
};
</script>
