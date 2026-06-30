import { endOfMonth, endOfYear, format, isAfter, isValid, parseISO, startOfMonth, startOfYear } from "date-fns";
import { WMSCapabilities } from "ol/format";
import { ILayer } from "@/types/layer";
import { ETimeSliderDisplayMode, ETimeSliderStepSize, IMapStore } from "@/types/mapStore";

export interface IWmsTimeRange {
  minDate: Date;
  maxDate: Date;
}

interface IWmsCapabilitiesLayer {
  Name?: string;
  Layer?: IWmsCapabilitiesLayer[];
  Dimension?: IWmsCapabilitiesTimeEntry[];
  Extent?: IWmsCapabilitiesTimeEntry[];
}

interface IWmsCapabilitiesTimeEntry {
  name?: string;
  values?: string;
}

interface IWmsCapabilitiesDocument {
  Capability?: {
    Layer?: IWmsCapabilitiesLayer;
  };
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
 * Parses a WMS time value into a date.
 * @param value - The WMS time value to parse.
 * @returns The parsed date, or null when the value is invalid.
 */
const parseWmsTimeDate = (value: string) => {
  const trimmedValue = value.trim();
  const date = parseISO(/^\d{4}-\d{2}-\d{2}$/.test(trimmedValue) ? `${trimmedValue}T00:00:00Z` : trimmedValue);

  return isValid(date) ? date : null;
};

/**
 * Creates the WMS GetCapabilities URL for a layer.
 * @param layer - The layer to request capabilities for.
 * @returns The GetCapabilities URL.
 */
const createWmsCapabilitiesUrl = (layer: ILayer) => {
  const url = new URL(layer.url);

  url.search = new URLSearchParams({
    SERVICE: "WMS",
    REQUEST: "GetCapabilities",
    VERSION: "1.3.0",
  }).toString();

  return url;
};

/**
 * Removes the workspace prefix from a layer name.
 * @param layerName - The layer name to normalize.
 * @returns The layer name without workspace prefix.
 */
const stripWorkspace = (layerName: string) => {
  return layerName.includes(":") ? layerName.split(":").pop() : layerName;
};

/**
 * Finds a layer in the WMS capabilities tree by layer name.
 * @param capabilitiesLayer - The capabilities layer to search in.
 * @param layerName - The configured layer name to find.
 * @returns The matching capabilities layer, or null when it is not found.
 */
const findCapabilitiesLayer = (
  capabilitiesLayer: IWmsCapabilitiesLayer | undefined,
  layerName: string,
): IWmsCapabilitiesLayer | null => {
  if (!capabilitiesLayer) {
    return null;
  }

  const normalizedCapabilityLayerName = stripWorkspace(capabilitiesLayer.Name ?? "");
  const normalizedLayerName = stripWorkspace(layerName);

  if (normalizedCapabilityLayerName === normalizedLayerName) {
    return capabilitiesLayer;
  }

  for (const childLayer of capabilitiesLayer.Layer ?? []) {
    const matchingLayer = findCapabilitiesLayer(childLayer, layerName);

    if (matchingLayer) {
      return matchingLayer;
    }
  }

  return null;
};

/**
 * Returns the raw WMS time dimension values from a capabilities layer.
 * @param capabilitiesLayer - The capabilities layer to inspect.
 * @returns The time dimension values, or null when no time dimension exists.
 */
const getTimeDimensionValues = (capabilitiesLayer: IWmsCapabilitiesLayer) => {
  const dimensions = [...(capabilitiesLayer.Dimension ?? []), ...(capabilitiesLayer.Extent ?? [])];
  const timeDimension = dimensions.find((dimension) => dimension.name?.toLowerCase() === "time");

  return timeDimension?.values ?? null;
};

/**
 * Parses WMS time dimension values into a min and max date range.
 * @param values - The raw WMS time dimension values.
 * @returns The parsed time range, or null when no valid dates exist.
 */
export const parseWmsTimeRange = (values: string): IWmsTimeRange | null => {
  const dates = values
    .split(",")
    .flatMap((value) => {
      const [startValue, endValue] = value.split("/");
      const startDate = startValue ? parseWmsTimeDate(startValue) : null;
      const endDate = endValue ? parseWmsTimeDate(endValue) : null;

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
 * Fetches WMS capabilities and extracts the time range for a layer.
 * @param layer - The layer to request capabilities for.
 * @param fetchOptions - Optional fetch options for authenticated requests.
 * @returns The WMS capabilities time range, or null when no range exists.
 */
export const getWmsCapabilitiesTimeRange = async (
  layer: ILayer,
  fetchOptions?: RequestInit,
): Promise<IWmsTimeRange | null> => {
  const response = await fetch(createWmsCapabilitiesUrl(layer), fetchOptions);

  if (!response.ok) {
    throw new Error("WMS capabilities konden niet opgehaald worden.");
  }

  const body = await response.text();

  if (!body) {
    return null;
  }

  const capabilities = new WMSCapabilities().read(body) as IWmsCapabilitiesDocument;
  const capabilitiesLayer = findCapabilitiesLayer(capabilities.Capability?.Layer, layer.name);

  if (!capabilitiesLayer) {
    return null;
  }

  const values = getTimeDimensionValues(capabilitiesLayer);

  return values ? parseWmsTimeRange(values) : null;
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
