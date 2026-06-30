<template>
  <Drawer
    :visible="showTimeSliderPanel"
    header="Tijdlijn bekijken"
    position="right"
    :pt="{
      mask: '!tw-bg-black/0',
    }"
    class="!tw-w-full md:!tw-w-[400px]"
    @update:visible="closePanel"
  >
    <div class="tw-flex tw-flex-col tw-gap-4">
      <ExplainerMessage>
        <template #icon>
          <InformationCircleIcon />
        </template>
        <template #explainer> Kies een kaartlaag met tijdgegevens en bekijk de data door de tijd. </template>
      </ExplainerMessage>

      <div class="tw-flex tw-flex-col tw-gap-2">
        <label for="time-slider-layer">Kaartlaag</label>
        <Select
          input-id="time-slider-layer"
          :model-value="selectedLayerId"
          :options="selectableLayers"
          filter
          name="time-slider-layer"
          option-label="title"
          option-value="id"
          placeholder="Selecteer kaartlaag"
          fluid
          :pt="{
            overlay: '!tw-max-w-48',
          }"
          @update:model-value="onSelectLayer"
        />
      </div>

      <div v-if="isReferenceDateEnabled" class="tw-flex tw-flex-col tw-gap-2">
        <label for="time-slider-display-mode">Weergave</label>
        <SelectButton
          input-id="time-slider-display-mode"
          :model-value="displayMode"
          :options="displayModeOptions"
          option-label="label"
          option-value="value"
          :allow-empty="false"
          class="time-slider-mode"
          @update:model-value="onSelectDisplayMode"
        />
      </div>

      <div class="tw-flex tw-flex-col tw-gap-2">
        <label>Sliderbereik</label>
        <ProgressSpinner
          v-if="mapStore.timeSliderCapabilitiesLoading"
          stroke-width="2"
          style="width: 50px; height: 50px"
        />
        <Message v-else-if="mapStore.timeSliderCapabilitiesError" severity="error">
          {{ mapStore.timeSliderCapabilitiesError }}</Message
        >
        <div v-else-if="canEditTimeSliderRange" class="tw-grid tw-grid-cols-[1fr_auto_1fr] tw-items-center tw-gap-2">
          <DatePicker
            :model-value="mapStore.timeSliderStartDate"
            input-id="time-slider-start-date"
            date-format="dd-mm-yy"
            placeholder="Startdatum"
            :min-date="mapStore.timeSliderMinDate ? mapStore.timeSliderMinDate : undefined"
            :max-date="mapStore.timeSliderMaxDate ? mapStore.timeSliderMaxDate : undefined"
            show-icon
            fluid
            @update:model-value="onSelectStartDate"
          />
          <span class="tw-text-slate-400">-</span>
          <DatePicker
            :model-value="mapStore.timeSliderEndDate"
            input-id="time-slider-end-date"
            date-format="dd-mm-yy"
            placeholder="Einddatum"
            :min-date="
              mapStore.timeSliderStartDate ? mapStore.timeSliderStartDate : mapStore.timeSliderMinDate || undefined
            "
            :max-date="mapStore.timeSliderMaxDate ? mapStore.timeSliderMaxDate : undefined"
            show-icon
            fluid
            @update:model-value="onSelectEndDate"
          />
        </div>
        <Message v-else severity="info">Selecteer een kaartlaag om het sliderbereik te bepalen.</Message>
      </div>

      <div class="tw-flex tw-flex-col tw-gap-2">
        <label for="time-slider-step-size">Stapgrootte</label>
        <Select
          input-id="time-slider-step-size"
          :model-value="stepSize"
          :options="stepSizeOptions"
          option-label="label"
          option-value="value"
          name="time-slider-step-size"
          placeholder="Selecteer stapgrootte"
          fluid
          @update:model-value="onSelectStepSize"
        />
      </div>
    </div>

    <template #footer>
      <div class="tw-flex tw-items-center tw-gap-2">
        <Button label="Verbergen" class="tw-flex-auto" outlined @click="closePanel">
          <ClosePanelIcon />
          Verbergen
        </Button>
        <Button class="tw-flex-auto" @click="disableTimeSlider">
          <i class="pi pi-history"></i>
          Tijdlijn uitschakelen
        </Button>
      </div>
    </template>
  </Drawer>
</template>

<script setup lang="ts">
import { computed, watch } from "vue";
import ClosePanelIcon from "@/assets/icons/close-panel-icon.svg";
import InformationCircleIcon from "@/assets/icons/information-circle-icon.svg";
import ExplainerMessage from "@/components/ExplainerMessage.vue";
import { ILayer } from "@/types/layer";
import { ETimeSliderDisplayMode, ETimeSliderStepSize } from "@/types/mapStore";
import { useGlobalStore } from "@/stores";
import { useMapStore } from "@/stores/map_store";

interface ISelectOption<TValue extends string> {
  label: string;
  value: TValue;
}

interface ITimeSliderPanelProps {
  mapId: string;
  layers: ILayer[];
  showTimeSliderPanel?: boolean;
}

const { mapId, layers, showTimeSliderPanel } = defineProps<ITimeSliderPanelProps>();

const emit = defineEmits<{
  (e: "close-panel"): void;
  (e: "disable-time-slider"): void;
}>();

const mapStore = useMapStore(mapId);
const globalStore = useGlobalStore();

const selectedLayerId = computed(() => mapStore.selectedTimeSliderLayerId);
const selectedLayer = computed(() => layers.find((layer) => layer.id === mapStore.selectedTimeSliderLayerId));
const displayMode = computed(() => mapStore.timeSliderDisplayMode);
const stepSize = computed(() => mapStore.timeSliderStepSize);
const isReferenceDateEnabled = computed(() => {
  return selectedLayer.value?.is_reference_date_enabled || false;
});
const canEditTimeSliderRange = computed(() => {
  return mapStore.timeSliderMinDate !== null && mapStore.timeSliderMaxDate !== null;
});

const displayModeOptions: ISelectOption<ETimeSliderDisplayMode>[] = [
  {
    label: "Periode",
    value: ETimeSliderDisplayMode.Period,
  },
  {
    label: "Peildatum",
    value: ETimeSliderDisplayMode.ReferenceDate,
  },
];

const stepSizeOptions: ISelectOption<ETimeSliderStepSize>[] = [
  {
    label: "Dag",
    value: ETimeSliderStepSize.Day,
  },
  {
    label: "Maand",
    value: ETimeSliderStepSize.Month,
  },
  {
    label: "Jaar",
    value: ETimeSliderStepSize.Year,
  },
];

const selectableLayers = computed(() => {
  return layers.filter((layer) => !layer.is_base && layer.is_time_enabled);
});

const loadSelectedLayerTimeRange = async () => {
  const layer = selectedLayer.value;

  if (!layer) {
    return;
  }

  await mapStore.loadTimeSliderCapabilitiesRange(layer, globalStore.user);
};

watch(selectedLayerId, loadSelectedLayerTimeRange, { immediate: true });

const closePanel = () => {
  emit("close-panel");
};

const disableTimeSlider = () => {
  mapStore.resetTimeSlider();
  emit("disable-time-slider");
};

const onSelectLayer = (layerId: string | null) => {
  if (!layerId) {
    mapStore.disableTimeSlider();
    return;
  }

  mapStore.toggleLayer({
    selectedLayerId: layerId,
    is_visible: true,
  });
};

const onSelectDisplayMode = (selectedDisplayMode: ETimeSliderDisplayMode) => {
  mapStore.setTimeSliderDisplayMode(selectedDisplayMode);
};

const onSelectStartDate = (startDate: Date | null | undefined) => {
  if (startDate === undefined) {
    mapStore.setTimeSliderStartDate(null);
    return;
  }

  mapStore.setTimeSliderStartDate(startDate);
};

const onSelectEndDate = (endDate: Date | null | undefined) => {
  if (endDate === undefined) {
    mapStore.setTimeSliderEndDate(null);
    return;
  }

  mapStore.setTimeSliderEndDate(endDate);
};

const onSelectStepSize = (selectedStepSize: ETimeSliderStepSize) => {
  mapStore.setTimeSliderStepSize(selectedStepSize);
};
</script>

<style scoped>
.time-slider-mode {
  width: 100%;
}

.time-slider-mode :deep(.p-togglebutton) {
  flex: 1;
}
</style>
