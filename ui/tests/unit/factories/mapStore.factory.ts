import { ETimeSliderDisplayMode, ETimeSliderStepSize, IMapStore } from "@/types/mapStore";

const createDefaultMapStore = (): IMapStore => ({
  layerFilters: {},
  leftSelectedCompareLayerId: null,
  rightSelectedCompareLayerId: null,
  comparePercentage: 50,
  timeSlider: false,
  showTimeSliderPanel: false,

  selectedTimeSliderLayerId: null,
  timeSliderDisplayMode: ETimeSliderDisplayMode.Period,
  timeSliderStartDate: new Date(2020, 5, 15),
  timeSliderEndDate: null,
  timeSliderMinDate: new Date(2020, 0, 1),
  timeSliderMaxDate: new Date(2024, 11, 31),
  timeSliderCapabilitiesLoading: false,
  timeSliderCapabilitiesError: null,
  timeSliderStepSize: ETimeSliderStepSize.Year,
  timeSliderReferenceDate: new Date(2024, 5, 15),
  timeSliderPeriodDates: [new Date(2020, 5, 15), new Date(2024, 5, 15)],

  cycloView: null,
  measuredAreas: [],
  layers: [],
  selectedBaseLayer: null,
  drawingId: null,
});

export const createMapStore = (overrides: Partial<IMapStore> = {}): IMapStore => ({
  ...createDefaultMapStore(),
  ...overrides,
});
