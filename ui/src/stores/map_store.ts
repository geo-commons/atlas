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
        const activeFilters = Object.entries(state.layerFilters).filter(([, layer]) =>
          Object.values(layer.filters || {}).some((filterArray) => filterArray.length > 0),
        );

        const count = activeFilters.reduce((totalCount, [, { filters }]) => {
          const activeCount = Object.values(filters).filter((array) => array.length > 0).length;
          return totalCount + activeCount;
        }, 0);

        return count;
      },
      getFiltersForLayer(state) {
        return (layerId: string) => {
          return state.layerFilters[layerId]?.filters || {};
        };
      },
      getActiveFilterCountForLayer(state) {
        return (layerId: string) => {
          const layerFilter = state.layerFilters[layerId];
          if (!layerFilter) return 0;

          return Object.values(layerFilter.filters).filter((array) => array.length > 0).length;
        };
      },
    },
  })();
}
