import { Geometry } from "ol/geom";
import { ILayer } from "@/types/layer";

export enum ELayerFilterSource {
  Legend = "legend",
  Panel = "panel",
}

export interface ILayerFilter {
  filters: {
    [key: string]: Array<string>;
  };
  searchQuery: string;
  legendFilters?: string[];
  source?: ELayerFilterSource;
}

export interface ICycloView {
  detail: {
    yaw: number;
    pitch: number;
    hFov: number;
  };
}

export interface ILayerFilters {
  // key is layer id
  [key: string]: ILayerFilter;
}

export enum ETimeSliderDisplayMode {
  Period = "period",
  ReferenceDate = "referenceDate",
}

export enum ETimeSliderStepSize {
  Day = "day",
  Month = "month",
  Year = "year",
}

export interface IMapStore {
  layerFilters: ILayerFilters;
  leftSelectedCompareLayerId: string | null;
  rightSelectedCompareLayerId: string | null;
  comparePercentage: number;
  timeSlider: boolean;
  showTimeSliderPanel: boolean;
  selectedTimeSliderLayerId: string | null;
  timeSliderDisplayMode: ETimeSliderDisplayMode;
  timeSliderStartDate: Date | null;
  timeSliderEndDate: Date | null;
  timeSliderMinDate: Date | null;
  timeSliderMaxDate: Date | null;
  timeSliderCapabilitiesLoading: boolean;
  timeSliderCapabilitiesError: string | null;
  timeSliderStepSize: ETimeSliderStepSize;
  timeSliderReferenceDate: Date;
  timeSliderPeriodDates: [Date, Date];
  cycloView: ICycloView | null;
  measuredAreas: Geometry[];
  layers: ILayer[];
  selectedBaseLayer: ILayer | null;
  drawingId: string | null;
}
