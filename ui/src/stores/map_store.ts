import { defineStore } from "pinia";

export interface ILayerFilter {
  filters: {
    [key: string]: Array<string>;
  };
  searchQuery: string;
}

export interface ILayerFilters {
  // key is layer id
  [key: string]: ILayerFilter;
}

interface IMapStore {
  layerFilters: ILayerFilters;
}

export function useMapStore(mapName: string) {
  return defineStore(`map-${mapName}`, {
    state: (): IMapStore => ({
      layerFilters: {},
    }),
    actions: {
      resetAllFilters() {
        this.layerFilters = {};
      },
      updateFiltersForLayer(layerId: string, filters: any) {
        this.layerFilters[layerId] = {
          ...this.layerFilters[layerId],
          filters: filters,
        };
      },
      updateSearchQueryForLayer(layerId: string, searchQuery: string) {
        this.layerFilters[layerId] = {
          ...this.layerFilters[layerId],
          searchQuery: searchQuery,
        };
      },
    },
    getters: {
      getActiveLayersWithFilterCount(state) {
        const activeFilters = Object.entries(state.layerFilters).filter(
          ([, layer]) =>
            Object.values(layer.filters || {}).some((filterArray) => filterArray.length > 0) ||
            (layer.searchQuery && layer.searchQuery.trim() !== ""),
        );

        const count = activeFilters.reduce((totalCount, [, { filters, searchQuery }]) => {
          const hasActiveFilters = filters ? Object.values(filters).some((array) => array.length > 0) : false;
          const hasSearchQuery = searchQuery && searchQuery.trim() !== "";
          const activeCount = hasActiveFilters || hasSearchQuery ? 1 : 0;
          return totalCount + activeCount;
        }, 0);

        return count;
      },
      getFiltersForLayer(state) {
        return (layerId: string) => {
          return state.layerFilters[layerId]?.filters || {};
        };
      },
      getSearchValueForLayer(state) {
        return (layerId: string): string => {
          const searchQuery = state.layerFilters[layerId]?.searchQuery || "";

          const value = searchQuery.match(/%([^%]+)%/);

          return value?.[1] || "";
        };
      },
      getActiveFilterCountForLayer(state) {
        return (layerId: string) => {
          const layerFilter = state.layerFilters[layerId];
          if (!layerFilter) return 0;

          // Get count of filters on specific layer
          let filterCount = layerFilter?.filters
            ? Object.values(layerFilter.filters).filter((array) => array.length > 0).length
            : 0;

          // If search with value is active on specific layer add this to count of filters
          if (layerFilter.searchQuery && layerFilter.searchQuery !== "") {
            filterCount += 1;
          }

          return filterCount;
        };
      },
    },
  })();
}
