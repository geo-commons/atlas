import { endOfMonth, endOfYear, format, isAfter, isValid, parseISO, startOfMonth, startOfYear } from "date-fns";
import { ILayer } from "@/types/layer";
import { ETimeSliderDisplayMode, ETimeSliderStepSize, IMapStore } from "@/types/mapStore";
import type { IOgcCollection } from "@/types/ogc";

export interface ITimeRange {
  minDate: Date;
  maxDate: Date;
}

/**
 * Formats a date as the start of that day in UTC.
 * @param date - The date to format.
 * @returns The formatted start date.
 */
const formatDateStart = (date: Date) => {
  return `${format(date, "yyyy-MM-dd")}T00:00:00.000Z`;
};

/**
 * Formats a date as the end of that day in UTC.
 * @param date - The date to format.
 * @returns The formatted end date.
 */
const formatDateEnd = (date: Date) => {
  return `${format(date, "yyyy-MM-dd")}T23:59:59.999Z`;
};

/**
 * Parses an OGC API time value into a date.
 * @param value - The OGC API time value to parse.
 * @returns The parsed date, or null when the value is invalid.
 */
const parseOgcTimeDate = (value: string) => {
  const trimmedValue = value.trim();
  const date = parseISO(/^\d{4}-\d{2}-\d{2}$/.test(trimmedValue) ? `${trimmedValue}T00:00:00Z` : trimmedValue);

  return isValid(date) ? date : null;
};

/**
 * Creates the GeoServer OGC API collection URL for a layer.
 * @param layer - The layer to request the collection document for.
 * @returns The OGC API collection URL.
 */
export const createOgcCollectionUrl = (layer: ILayer) => {
  const url = new URL(layer.url);
  const geoserverPathIndex = url.pathname.indexOf("/geoserver");
  const basePath = geoserverPathIndex === -1 ? "" : url.pathname.slice(0, geoserverPathIndex + "/geoserver".length);

  url.pathname = `${basePath}/ogc/maps/v1/collections/${layer.name}`;
  url.search = new URLSearchParams({ f: "application/json" }).toString();

  return url;
};

/**
 * Parses an OGC API collection temporal extent into a min and max date range.
 * @param collection - The OGC API collection document.
 * @returns The parsed time range, or null when no valid dates exist.
 */
export const parseOgcTimeRange = (collection: IOgcCollection): ITimeRange | null => {
  const dates = (collection.extent?.temporal?.interval ?? [])
    .flatMap(([startValue, endValue]) => {
      const startDate = startValue ? parseOgcTimeDate(startValue) : null;
      const endDate = endValue ? parseOgcTimeDate(endValue) : null;

      return [startDate, endDate].filter((date): date is Date => date !== null);
    })
    .sort((dateA, dateB) => dateA.getTime() - dateB.getTime());

  if (dates.length === 0) {
    return null;
  }

  const minDate = dates[0];
  const maxDate = dates[dates.length - 1];

  if (isAfter(minDate, maxDate)) {
    return null;
  }

  return { minDate, maxDate };
};

/**
 * Fetches the time range for a layer from the GeoServer OGC API collection document.
 * @param layer - The layer to request time metadata for.
 * @param fetchOptions - Optional fetch options for authenticated requests.
 * @returns The layer time range, or null when no range exists.
 */
export const getLayerTimeRange = async (layer: ILayer, fetchOptions?: RequestInit): Promise<ITimeRange | null> => {
  const response = await fetch(createOgcCollectionUrl(layer), fetchOptions);

  if (!response.ok) {
    throw new Error("OGC API collectie kon niet opgehaald worden.");
  }

  const collection = (await response.json()) as IOgcCollection;

  return parseOgcTimeRange(collection);
};

/**
 * Returns the first date for the selected time step.
 * @param date - The date to adjust.
 * @param stepSize - The selected time step size.
 * @returns The start date for the time step.
 */
const createStepStartDate = (date: Date, stepSize: ETimeSliderStepSize) => {
  if (stepSize === ETimeSliderStepSize.Year) {
    return startOfYear(date);
  }

  if (stepSize === ETimeSliderStepSize.Month) {
    return startOfMonth(date);
  }

  return date;
};

/**
 * Returns the last date for the selected time step.
 * @param date - The date to adjust.
 * @param stepSize - The selected time step size.
 * @returns The end date for the time step.
 */
const createStepEndDate = (date: Date, stepSize: ETimeSliderStepSize) => {
  if (stepSize === ETimeSliderStepSize.Year) {
    return endOfYear(date);
  }

  if (stepSize === ETimeSliderStepSize.Month) {
    return endOfMonth(date);
  }

  return date;
};

/**
 * Formats the reference date for the WMS time parameter.
 * @param date - The selected reference date.
 * @param state - The map store state.
 * @returns The formatted WMS reference time.
 */
const formatReferenceTime = (date: Date, state: IMapStore) => {
  const startDate = createStepStartDate(date, state.timeSliderStepSize);

  return formatDateStart(startDate);
};

/**
 * Formats a date period for the WMS time parameter.
 * @param startDate - The first selected date.
 * @param endDate - The second selected date.
 * @param stepSize - The selected time step size.
 * @returns The formatted WMS period time.
 */
const formatPeriodTime = ([startDate, endDate]: [Date, Date], stepSize: ETimeSliderStepSize) => {
  const sortedStartDate = startDate <= endDate ? startDate : endDate;
  const sortedEndDate = startDate <= endDate ? endDate : startDate;
  const stepStartDate = createStepStartDate(sortedStartDate, stepSize);
  const stepEndDate = createStepEndDate(sortedEndDate, stepSize);

  return `${formatDateStart(stepStartDate)}/${formatDateEnd(stepEndDate)}`;
};

/**
 * Returns the WMS time parameter for the selected time slider layer.
 * @param state - The map store state.
 * @param layerId - The layer id to check.
 * @param isTimeEnabled - Whether time is enabled for the layer.
 * @returns The WMS time parameter, or null when it should not be used.
 */
export const getWmsTimeParameter = (state: IMapStore, layerId: string, isTimeEnabled: boolean): string | null => {
  if (!isTimeEnabled) {
    return null;
  }

  if (state.selectedTimeSliderLayerId !== layerId) {
    return null;
  }

  if (state.timeSliderCapabilitiesLoading || state.timeSliderCapabilitiesError) {
    return null;
  }

  if (!state.timeSliderMinDate || !state.timeSliderMaxDate) {
    return null;
  }

  if (state.timeSliderDisplayMode === ETimeSliderDisplayMode.ReferenceDate) {
    return formatReferenceTime(state.timeSliderReferenceDate, state);
  }

  return formatPeriodTime(state.timeSliderPeriodDates, state.timeSliderStepSize);
};

/**
 * Returns a WFS CQL filter matching the active time slider period for a layer.
 * @param state - The map store state.
 * @param layer - The layer to check.
 * @returns The CQL filter, or null when it should not be used.
 */
export const getWfsTimeCqlFilter = (state: IMapStore, layer: ILayer): string | null => {
  if (!layer.is_time_enabled) {
    return null;
  }

  if (state.selectedTimeSliderLayerId !== layer.id) {
    return null;
  }

  if (state.timeSliderCapabilitiesLoading || state.timeSliderCapabilitiesError) {
    return null;
  }

  if (!state.timeSliderMinDate || !state.timeSliderMaxDate) {
    return null;
  }

  const startField = layer.time_slider_start_field?.trim();
  const endField = layer.time_slider_end_field?.trim();

  if (!startField) {
    return null;
  }

  let selectedStartDate: string;
  let selectedEndDate: string;

  if (state.timeSliderDisplayMode === ETimeSliderDisplayMode.ReferenceDate) {
    selectedStartDate = formatDateStart(createStepStartDate(state.timeSliderReferenceDate, state.timeSliderStepSize));

    if (endField) {
      return `(${startField} <= '${selectedStartDate}' AND ${endField} >= '${selectedStartDate}')`;
    }

    return `${startField} = '${selectedStartDate}'`;
  } else {
    const [startDate, endDate] = state.timeSliderPeriodDates;
    const sortedStartDate = startDate <= endDate ? startDate : endDate;
    const sortedEndDate = startDate <= endDate ? endDate : startDate;

    selectedStartDate = formatDateStart(createStepStartDate(sortedStartDate, state.timeSliderStepSize));
    selectedEndDate = formatDateEnd(createStepEndDate(sortedEndDate, state.timeSliderStepSize));
  }

  if (endField) {
    return `(${startField} <= '${selectedEndDate}' AND ${endField} >= '${selectedStartDate}')`;
  }

  return `(${startField} >= '${selectedStartDate}' AND ${startField} <= '${selectedEndDate}')`;
};
