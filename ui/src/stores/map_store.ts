import { defineStore } from "pinia";
import { ELayerTypes, ILayer, ISelectedLayerProps } from "@/types/layer";
import { ICycloView, IMapStore } from "@/types/mapStore";
import { Geometry } from "ol/geom";

const visibleSourceTypes = [ELayerTypes.WMS_WFS, ELayerTypes.WFS];

export function useMapStore(mapName: string) {
  return defineStore(`map-${mapName}`, {
    state: (): IMapStore => ({
      layerFilters: {},
      leftSelectedCompareLayerId: null,
      rightSelectedCompareLayerId: null,
      comparePercentage: 50,
      cycloView: null,
      measuredAreas: [],
      layers: [],
      selectedBaseLayer: null,
      drawingId: null,
    }),
    actions: {
      resetAllFilters() {
        this.layerFilters = {};
      },
      resetFiltersForLayer(layerId: string) {
        this.layerFilters[layerId] = {
          filters: {},
          searchQuery: "",
        };
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
      setLeftSelectedCompareLayerId(selectedLayers: string | null) {
        this.leftSelectedCompareLayerId = selectedLayers;
      },
      setRightSelectedCompareLayerId(selectedLayers: string | null) {
        this.rightSelectedCompareLayerId = selectedLayers;
      },
      setComparePercentage(swipe: number) {
        this.comparePercentage = swipe;
      },
      setCycloView(cycloView: ICycloView | null) {
        this.cycloView = cycloView;
      },
      addMeasuredArea(area: Geometry) {
        this.measuredAreas.push(area);
      },
      clearMeasuredAreas() {
        this.measuredAreas = [];
      },
      setLayers(layers: ILayer[]) {
        this.layers = layers;
      },
      setBaseLayer(layer: ILayer) {
        this.selectedBaseLayer = layer;
      },
      deselectBaseLayer() {
        if (this.selectedBaseLayer) {
          this.selectedBaseLayer.is_visible = false;
          this.selectedBaseLayer = null;
        }
      },
      updateLayer(id: string, updater: (layer: ILayer) => void) {
        const layer = this.layers.find((l) => l.id === id);
        if (layer) {
          updater(layer);
        }
      },
      toggleBaseLayer(selectedLayerProps: ISelectedLayerProps) {
        const layer = this.layers.find((l) => l.id === selectedLayerProps.selectedLayerId);

        if (layer) {
          layer.is_visible = selectedLayerProps.is_visible;

          if (this.selectedBaseLayer) {
            this.selectedBaseLayer.is_visible = false;
          }
          this.selectedBaseLayer = layer;
        }
      },
      toggleLayer(selectedLayerProps: ISelectedLayerProps) {
        this.updateLayer(selectedLayerProps.selectedLayerId, (layer) => {
          layer.is_visible = selectedLayerProps.is_visible;
        });

        this.resetFiltersForLayer(selectedLayerProps.selectedLayerId);
      },
      setLayerOpacity(selectedLayerProps: ISelectedLayerProps) {
        this.updateLayer(selectedLayerProps.selectedLayerId, (layer) => {
          layer.opacity = selectedLayerProps.opacity;
        });
      },
      toggleLayerisSelectable(selectedLayerProps: ISelectedLayerProps) {
        this.updateLayer(selectedLayerProps.selectedLayerId, (layer) => {
          layer.is_selectable = selectedLayerProps.is_selectable;
        });
      },
      setDrawingId(drawingId: string) {
        this.drawingId = drawingId;
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
      // Returns the total count of selected items in each filter passed in the selectFilters array
      getActiveSelectedItemCountPerFilterForLayer(state) {
        return (layerId: string, selectedFilters: string[]) => {
          let count: number = 0;
          const layerFilter = state.layerFilters[layerId];

          if (layerFilter) {
            const filtersWithItemsToCount = Object.fromEntries(
              Object.entries(layerFilter.filters).filter(([key]) => selectedFilters.includes(key)),
            );

            const filterItems = Object.values(filtersWithItemsToCount);

            filterItems.map((item) => {
              count += item.length;
            });
          }

          return count;
        };
      },
      baseLayers: (state) => {
        return state.layers.filter((layer) => layer.is_base);
      },
      regularLayers: (state) => {
        return state.layers.filter((layer) => !layer.is_base);
      },
      wmsWfsLayers: (state) => {
        return state.layers.filter((l) => !l.is_base && (l.source_type === "WMS" || l.source_type === "WMS_WFS"));
      },
      visibleLayers: (state) => {
        return state.layers.filter((layer) => layer.category && layer.is_visible && !layer.is_base);
      },
      visibleLayersForFeatures: (state) => {
        return state.layers.filter((layer) => layer.is_selectable && !layer.is_base && layer.is_visible);
      },
      visibleLayersForDataPanel: (state) => {
        return state.layers.filter(
          (layer) =>
            layer.is_visible &&
            !layer.is_base &&
            layer.show_in_detail_panel &&
            visibleSourceTypes.includes(layer.source_type),
        );
      },
      visibleLayersForDetailPanel: (state) => {
        return state.layers.filter((layer) => layer.is_visible && layer.show_in_detail_panel && !layer.is_base);
      },
    },
  })();
}
