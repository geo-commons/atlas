import type { ILayerFilters } from "@/types/mapStore";

export const getLayerCqlFilter = (layerFilters: ILayerFilters, layerId: string): string | null => {
  const layerFilter = layerFilters[layerId];

  if (!layerFilter) {
    return null;
  }

  const cqlFilters: string[] = [];

  if (layerFilter.searchQuery) {
    cqlFilters.push(layerFilter.searchQuery);
  }

  Object.entries(layerFilter.filters || {}).forEach(([filterKey, filterValues]) => {
    if (filterValues.length === 0) {
      return;
    }

    const values = filterValues
      .filter((filterValue) => filterValue !== "Leeg")
      .map((filterValue) => `'${filterValue}'`)
      .join(",");

    const valueFilters: string[] = [];

    if (filterValues.includes("Leeg")) {
      valueFilters.push(`(${filterKey} IS NULL or ${filterKey} = '')`);
    }

    if (values.length > 0) {
      valueFilters.push(`${filterKey} IN (${values})`);
    }

    if (valueFilters.length > 0) {
      cqlFilters.push(`(${valueFilters.join(" OR ")})`);
    }
  });

  return cqlFilters.length > 0 ? cqlFilters.join(" AND ") : null;
};
