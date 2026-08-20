import {
  ELayerFilterOperator,
  type ILayerFilters,
  type ILayerPropertyFilter,
  type TLayerFilterValue,
} from "@/types/mapStore";

const emptyFilterValue = "Leeg";

const isLayerPropertyFilter = (
  filterValue: Array<TLayerFilterValue> | ILayerPropertyFilter,
): filterValue is ILayerPropertyFilter => {
  return !Array.isArray(filterValue) && "operator" in filterValue && Array.isArray(filterValue.values);
};

const escapeCqlString = (value: string): string => value.replace(/'/g, "''");

const formatCqlValue = (value: TLayerFilterValue, quoteStrings = true): string => {
  if (typeof value === "number") {
    return value.toString();
  }

  const trimmedValue = value.trim();

  if (!quoteStrings && trimmedValue !== "" && !Number.isNaN(Number(trimmedValue))) {
    return trimmedValue;
  }

  return `'${escapeCqlString(value)}'`;
};

const getValueListFilter = (filterKey: string, filterValues: TLayerFilterValue[]): string | null => {
  if (filterValues.length === 0) {
    return null;
  }

  const values = filterValues
    .filter((filterValue) => filterValue !== emptyFilterValue)
    .map((filterValue) => formatCqlValue(filterValue))
    .join(",");

  const valueFilters: string[] = [];

  if (filterValues.includes(emptyFilterValue)) {
    valueFilters.push(`(${filterKey} IS NULL or ${filterKey} = '')`);
  }

  if (values.length > 0) {
    valueFilters.push(`${filterKey} IN (${values})`);
  }

  return valueFilters.length > 0 ? `(${valueFilters.join(" OR ")})` : null;
};

export const getLayerPropertyCqlFilter = (
  filterKey: string,
  filterValue: Array<TLayerFilterValue> | ILayerPropertyFilter,
): string | null => {
  if (!isLayerPropertyFilter(filterValue)) {
    return getValueListFilter(filterKey, filterValue);
  }

  const values = filterValue.values.filter((value) => value !== "" || filterValue.operator.includes("NULL"));

  if (filterValue.operator === ELayerFilterOperator.IsNull) {
    return `(${filterKey} IS NULL or ${filterKey} = '')`;
  }

  if (filterValue.operator === ELayerFilterOperator.IsNotNull) {
    return `(${filterKey} IS NOT NULL AND ${filterKey} <> '')`;
  }

  if (values.length === 0) {
    return null;
  }

  if (filterValue.operator === ELayerFilterOperator.In || filterValue.operator === ELayerFilterOperator.NotIn) {
    const valueListFilter = getValueListFilter(filterKey, values);

    if (filterValue.operator === ELayerFilterOperator.In) {
      return valueListFilter;
    }

    const nonEmptyValues = values.filter((value) => value !== emptyFilterValue).map((value) => formatCqlValue(value));
    const valueFilters: string[] = [];

    if (values.includes(emptyFilterValue)) {
      valueFilters.push(`(${filterKey} IS NOT NULL AND ${filterKey} <> '')`);
    }

    if (nonEmptyValues.length > 0) {
      valueFilters.push(`${filterKey} NOT IN (${nonEmptyValues.join(",")})`);
    }

    return valueFilters.length > 0 ? `(${valueFilters.join(" AND ")})` : null;
  }

  const value = values[0];

  if (filterValue.operator === ELayerFilterOperator.Like || filterValue.operator === ELayerFilterOperator.ILike) {
    return `${filterKey} ${filterValue.operator} '%${escapeCqlString(String(value))}%'`;
  }

  return `${filterKey} ${filterValue.operator} ${formatCqlValue(value, false)}`;
};

export const getLayerCqlFilter = (layerFilters: ILayerFilters, layerId: string): string | null => {
  const layerFilter = layerFilters[layerId];

  if (!layerFilter) {
    return null;
  }

  const cqlFilters: string[] = [];

  if (layerFilter.searchQuery) {
    cqlFilters.push(layerFilter.searchQuery);
  }

  const rawCqlFilters = Object.values(layerFilter.rawCqlFilters || {}).filter((filter) => filter.trim() !== "");

  if (rawCqlFilters.length > 0) {
    cqlFilters.push(`(${rawCqlFilters.map((filter) => `(${filter})`).join(" OR ")})`);
  }

  Object.entries(layerFilter.filters || {}).forEach(([filterKey, filterValues]) => {
    const propertyFilter = getLayerPropertyCqlFilter(filterKey, filterValues);

    if (propertyFilter) {
      cqlFilters.push(propertyFilter);
    }
  });

  return cqlFilters.length > 0 ? cqlFilters.join(" AND ") : null;
};
