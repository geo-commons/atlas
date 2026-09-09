import { ELayerFilterSource, EPanelFilterOperator } from "@/types/mapStore";
import type { ILayerFilters, IPanelFilterValue } from "@/types/mapStore";

// All possible DescribeFeatureType localType values are based on
// https://github.com/geoserver/geoserver/blob/main/src/wfs-core/src/main/java/org/geoserver/wfs/json/JSONDescribeFeatureTypeResponse.java#L132
export const TEXT_TYPES = ["string"];
export const NUMERIC_TYPES = ["int", "number"];
export const BOOLEAN_TYPES = ["boolean"];
export const TEMPORAL_TYPES = ["date", "time", "date-time"];

const escapeStringValue = (value: string): string => value.replace(/'/g, "''");

export const normalizeType = (type?: string): string | undefined => type?.toLowerCase().replace(/^(xsd|xs):/, "");

const isTextType = (type?: string): boolean => {
  const normalizedType = normalizeType(type);

  return !normalizedType || TEXT_TYPES.includes(normalizedType);
};

const isNumericType = (type?: string): boolean => {
  const normalizedType = normalizeType(type);

  return !!normalizedType && NUMERIC_TYPES.includes(normalizedType);
};

const isBooleanType = (type?: string): boolean => {
  const normalizedType = normalizeType(type);

  return !!normalizedType && BOOLEAN_TYPES.includes(normalizedType);
};

const isTemporalType = (type?: string): boolean => {
  const normalizedType = normalizeType(type);

  return !!normalizedType && TEMPORAL_TYPES.includes(normalizedType);
};

const formatCqlValue = (value: string | number | null | undefined, type?: string): string | null => {
  if (value === null || value === undefined || value === "") {
    return null;
  }

  if (isBooleanType(type)) {
    return String(value).toLowerCase();
  }

  if (isTemporalType(type)) {
    return String(value);
  }

  if (typeof value === "number" || isNumericType(type)) {
    return String(value);
  }

  return `'${escapeStringValue(String(value))}'`;
};

const buildEmptyFilter = (filterKey: string, type?: string): string => {
  if (isTextType(type)) {
    return `(${filterKey} IS NULL OR ${filterKey} = '')`;
  }

  return `${filterKey} IS NULL`;
};

const buildNotEmptyFilter = (filterKey: string, type?: string): string => {
  if (isTextType(type)) {
    return `(${filterKey} IS NOT NULL AND ${filterKey} <> '')`;
  }

  return `${filterKey} IS NOT NULL`;
};

const getComparisonOperator = (operator: EPanelFilterOperator): string | null => {
  switch (operator) {
    case EPanelFilterOperator.Equals:
      return "=";
    case EPanelFilterOperator.NotEquals:
      return "<>";
    case EPanelFilterOperator.GreaterThan:
      return ">";
    case EPanelFilterOperator.GreaterThanOrEqual:
      return ">=";
    case EPanelFilterOperator.LessThan:
      return "<";
    case EPanelFilterOperator.LessThanOrEqual:
      return "<=";
    default:
      return null;
  }
};

const buildPanelFilterCql = (filterKey: string, filterValue: IPanelFilterValue): string | null => {
  switch (filterValue.operator) {
    case EPanelFilterOperator.Empty:
      return buildEmptyFilter(filterKey, filterValue.type);
    case EPanelFilterOperator.NotEmpty:
      return buildNotEmptyFilter(filterKey, filterValue.type);
    default:
      break;
  }

  const values = filterValue.values
    .map((value) => formatCqlValue(value, filterValue.type))
    .filter((value): value is string => value !== null);

  if (values.length === 0) {
    return null;
  }

  if (filterValue.operator === EPanelFilterOperator.Equals && values.length > 1) {
    return `${filterKey} IN (${values.join(",")})`;
  }

  const cqlOperator = getComparisonOperator(filterValue.operator);

  if (!cqlOperator) {
    return null;
  }

  return `${filterKey} ${cqlOperator} ${values[0]}`;
};

export const getLayerCqlFilter = (layerFilters: ILayerFilters, layerId: string): string | null => {
  const layerFilter = layerFilters[layerId];

  if (!layerFilter) {
    return null;
  }

  const cqlFilters: string[] = [];

  if (layerFilter.source === ELayerFilterSource.Legend && layerFilter.legendFilters.length) {
    return layerFilter.legendFilters.map((legendFilter) => `(${legendFilter})`).join(" OR ");
  }

  if (layerFilter.searchQuery) {
    cqlFilters.push(layerFilter.searchQuery);
  }

  Object.entries(layerFilter.filters || {}).forEach(([filterKey, filterValue]) => {
    const panelFilterCql = buildPanelFilterCql(filterKey, filterValue);

    if (panelFilterCql) {
      cqlFilters.push(panelFilterCql);
    }
  });

  return cqlFilters.length > 0 ? cqlFilters.join(" AND ") : null;
};
