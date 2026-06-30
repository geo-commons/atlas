<template>
  <div
    v-if="
      showTimeSlider &&
      mapStore.timeSliderMinDate &&
      mapStore.timeSliderMaxDate &&
      !mapStore.timeSliderCapabilitiesError
    "
    class="tw-flex tw-items-center tw-gap-4 tw-bg-white tw-h-14 tw-px-4 tw-rounded-sm tw-shadow-md time-slider"
  >
    <span class="tw-text-xs tw-font-semibold tw-text-slate-500 tw-w-16 tw-text-right tw-select-none">{{
      minLabel
    }}</span>
    <div class="tw-relative tw-flex-1 tw-px-1">
      <span class="time-slider-tooltip" :style="{ left: `${tooltipPosition}%` }">{{ tooltipLabel }}</span>
      <Slider
        v-if="mapStore.timeSliderDisplayMode === ETimeSliderDisplayMode.Period"
        :model-value="activePeriodSteps"
        :min="0"
        :max="maxStep"
        :step="1"
        range
        class="tw-w-full"
        @update:model-value="onPeriodStepsChange"
      />
      <Slider
        v-else
        :model-value="activeReferenceStep"
        :min="0"
        :max="maxStep"
        :step="1"
        class="tw-w-full"
        @update:model-value="onReferenceStepChange"
      />
    </div>
    <span class="tw-text-xs tw-font-semibold tw-text-slate-500 tw-w-16 tw-select-none">{{ maxLabel }}</span>
  </div>
</template>

<script setup lang="ts">
import {
  addDays,
  addMonths,
  addYears,
  differenceInCalendarDays,
  differenceInCalendarMonths,
  differenceInCalendarYears,
  format,
  startOfDay,
} from "date-fns";
import { useThrottleFn } from "@vueuse/core";
import { computed, ref, watch } from "vue";
import { useMapStore } from "@/stores/map_store";
import { ETimeSliderDisplayMode, ETimeSliderStepSize } from "@/types/mapStore";

const DEFAULT_MIN_YEAR = 0;
const DEFAULT_MAX_YEAR = new Date().getFullYear();
const TIME_SLIDER_COMMIT_THROTTLE_MS = 150;

interface ITimeSliderSliderProps {
  mapId: string;
  showTimeSlider: boolean;
}

const { mapId, showTimeSlider } = defineProps<ITimeSliderSliderProps>();

const mapStore = useMapStore(mapId);

// Keep drag state local so the slider stays responsive while store commits are throttled.
const draftReferenceStep = ref<number | null>(null);
const draftPeriodSteps = ref<[number, number] | null>(null);

const getDate = (date: Date | null, fallbackDate: Date) => {
  return startOfDay(date instanceof Date ? date : fallbackDate);
};

const minDate = computed(() => {
  return getDate(mapStore.timeSliderStartDate ?? mapStore.timeSliderMinDate, new Date(DEFAULT_MIN_YEAR, 0, 1));
});

const maxDate = computed(() => {
  const endDate = getDate(mapStore.timeSliderEndDate ?? mapStore.timeSliderMaxDate, new Date(DEFAULT_MAX_YEAR, 11, 31));

  if (endDate > minDate.value) {
    return endDate;
  }

  return addStep(minDate.value, 1);
});

const formatDate = (date: Date) => {
  if (mapStore.timeSliderStepSize === ETimeSliderStepSize.Year) {
    return format(date, "yyyy");
  }

  if (mapStore.timeSliderStepSize === ETimeSliderStepSize.Month) {
    return format(date, "MM-yyyy");
  }

  return format(date, "dd-MM-yyyy");
};

const addStep = (date: Date, steps: number) => {
  if (mapStore.timeSliderStepSize === ETimeSliderStepSize.Year) {
    return addYears(date, steps);
  }

  if (mapStore.timeSliderStepSize === ETimeSliderStepSize.Month) {
    return addMonths(date, steps);
  }

  return addDays(date, steps);
};

const getStepDiff = (startDate: Date, endDate: Date) => {
  if (mapStore.timeSliderStepSize === ETimeSliderStepSize.Year) {
    return differenceInCalendarYears(endDate, startDate);
  }

  if (mapStore.timeSliderStepSize === ETimeSliderStepSize.Month) {
    return differenceInCalendarMonths(endDate, startDate);
  }

  return differenceInCalendarDays(endDate, startDate);
};

const clampStep = (step: number) => {
  return Math.min(Math.max(step, 0), maxStep.value);
};

const getDateStep = (date: Date) => {
  return clampStep(getStepDiff(minDate.value, date));
};

const getStepPosition = (step: number) => {
  if (maxStep.value === 0) {
    return 0;
  }

  return (clampStep(step) / maxStep.value) * 100;
};

const maxStep = computed(() => {
  return Math.max(getStepDiff(minDate.value, maxDate.value), 1);
});

const minLabel = computed(() => {
  return formatDate(minDate.value);
});

const maxLabel = computed(() => {
  return formatDate(maxDate.value);
});

const referenceStep = computed(() => {
  return getDateStep(mapStore.timeSliderReferenceDate);
});

const periodSteps = computed<[number, number]>(() => {
  const [startDate, endDate] = mapStore.timeSliderPeriodDates;
  const startStep = getDateStep(startDate);
  const endStep = getDateStep(endDate);

  return [Math.min(startStep, endStep), Math.max(startStep, endStep)];
});

// Labels and handle positions use draft values while dragging, then fall back to committed store values.
const activeReferenceStep = computed(() => {
  return draftReferenceStep.value ?? referenceStep.value;
});

const activePeriodSteps = computed<[number, number]>(() => {
  return draftPeriodSteps.value ?? periodSteps.value;
});

const tooltipLabel = computed(() => {
  if (mapStore.timeSliderDisplayMode === ETimeSliderDisplayMode.Period) {
    const startLabel = formatDate(addStep(minDate.value, activePeriodSteps.value[0]));
    const endLabel = formatDate(addStep(minDate.value, activePeriodSteps.value[1]));

    return `${startLabel} - ${endLabel}`;
  }

  return formatDate(addStep(minDate.value, activeReferenceStep.value));
});

const tooltipPosition = computed(() => {
  if (mapStore.timeSliderDisplayMode === ETimeSliderDisplayMode.Period) {
    return (getStepPosition(activePeriodSteps.value[0]) + getStepPosition(activePeriodSteps.value[1])) / 2;
  }

  return getStepPosition(activeReferenceStep.value);
});

const getPeriodSteps = (selectedSteps: number | number[]): [number, number] | null => {
  if (!Array.isArray(selectedSteps)) {
    return null;
  }

  return [selectedSteps[0], selectedSteps[1]];
};

const commitPeriodSteps = (steps: [number, number]) => {
  mapStore.setTimeSliderPeriodDates([addStep(minDate.value, steps[0]), addStep(minDate.value, steps[1])]);
};

const commitReferenceStep = (step: number) => {
  mapStore.setTimeSliderReferenceDate(addStep(minDate.value, step));
};

const throttledCommitPeriodSteps = useThrottleFn(commitPeriodSteps, TIME_SLIDER_COMMIT_THROTTLE_MS, false, true);
const throttledCommitReferenceStep = useThrottleFn(commitReferenceStep, TIME_SLIDER_COMMIT_THROTTLE_MS, false, true);

const clearDraftSteps = () => {
  draftReferenceStep.value = null;
  draftPeriodSteps.value = null;
};

const onPeriodStepsChange = (selectedSteps: number | number[]) => {
  const steps = getPeriodSteps(selectedSteps);

  if (!steps) {
    return;
  }

  draftPeriodSteps.value = steps;
  throttledCommitPeriodSteps(steps);
};

const onReferenceStepChange = (selectedStep: number | number[]) => {
  if (Array.isArray(selectedStep)) {
    return;
  }

  draftReferenceStep.value = selectedStep;
  throttledCommitReferenceStep(selectedStep);
};

// Clear local drag state when the time-slider configuration changes externally.
watch(
  () => [
    mapStore.selectedTimeSliderLayerId,
    mapStore.timeSliderDisplayMode,
    mapStore.timeSliderStepSize,
    mapStore.timeSliderMinDate,
    mapStore.timeSliderMaxDate,
  ],
  clearDraftSteps,
  { deep: true },
);
</script>

<style scoped>
.time-slider {
  width: min(520px, calc(100vw - (var(--padding-screen) * 2)));
}

.time-slider-tooltip {
  position: absolute;
  top: -30px;
  transform: translateX(-50%);
  padding: 4px 8px;
  border-radius: var(--radius-normal);
  background: var(--color-primary);
  color: var(--color-white);
  font-size: 11px;
  font-weight: var(--font-weight-bold);
  line-height: 1;
  white-space: nowrap;
}

.time-slider-tooltip::after {
  content: "";
  position: absolute;
  left: 50%;
  bottom: -4px;
  transform: translateX(-50%);
  border-top: 4px solid var(--color-primary);
  border-left: 4px solid transparent;
  border-right: 4px solid transparent;
}
</style>
