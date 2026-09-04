import { defineStore } from "pinia";
import { ELayerTypes } from "@/types/layer";
import type {
  ILayer,
  ILayerOrderDetails,
  ISetLayerOpacityProps,
  IToggleLayerProps,
  IToggleLayerSelectableProps,
} from "@/types/layer";
import {
  ELayerFilterSource,
  ETimeSliderDisplayMode,
  ETimeSliderStepSize,
  ICycloView,
  IMapStore,
} from "@/types/mapStore";
import { getFetchParameters } from "@/utils/auth";
import { getLayerTimeRange } from "@/utils/wms-time";
import type { IUser } from "@/types/user";
import { Geometry } from "ol/geom";

const visibleSourceTypes = [ELayerTypes.WMS_WFS, ELayerTypes.WFS];
const createDefaultTimeSliderStartDate = () => new Date(1969, 0, 1);
const createDefaultTimeSliderEndDate = () => new Date();

const cloneDate = (date: Date) => new Date(date);

const getLayerDefaultTimeSliderDisplayMode = (layer: ILayer | undefined) => {
  if (
    layer?.is_reference_date_enabled &&
    layer.time_slider_default_display_mode === ETimeSliderDisplayMode.ReferenceDate
  ) {
    return ETimeSliderDisplayMode.ReferenceDate;
  }

  return ETimeSliderDisplayMode.Period;
};

export function useMapStore(mapName: string) {
  return defineStore(`map-${mapName}`, {
    state: (): IMapStore => ({
      layerFilters: {},
      leftSelectedCompareLayerId: null,
      rightSelectedCompareLayerId: null,
      comparePercentage: 50,
      timeSlider: false,
      showTimeSliderPanel: false,
      selectedTimeSliderLayerId: null,
      timeSliderDisplayMode: ETimeSliderDisplayMode.Period,
      timeSliderStartDate: createDefaultTimeSliderStartDate(),
      timeSliderEndDate: createDefaultTimeSliderEndDate(),
      timeSliderMinDate: null,
      timeSliderMaxDate: null,
      timeSliderCapabilitiesLoading: false,
      timeSliderCapabilitiesError: null,
      timeSliderStepSize: ETimeSliderStepSize.Year,
      timeSliderReferenceDate: createDefaultTimeSliderStartDate(),
      timeSliderPeriodDates: [createDefaultTimeSliderStartDate(), createDefaultTimeSliderEndDate()],
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
          legendFilters: [],
        };
      },
      // Panel/search filters and legend filters are mutually exclusive.
      // Updating one source clears the other so CQL filters are never combined accidentally.
      updateFiltersForLayer(layerId: string, filters: any) {
        this.layerFilters[layerId] = {
          ...this.layerFilters[layerId],
          filters: filters,
          legendFilters: [],
          source: ELayerFilterSource.Panel,
        };
      },
      updateLegendFiltersForLayer(layerId: string, legendFilters: string[]) {
        this.layerFilters[layerId] = {
          ...this.layerFilters[layerId],
          filters: {},
          searchQuery: "",
          legendFilters: legendFilters,
          source: ELayerFilterSource.Legend,
        };
      },
      updateSearchQueryForLayer(layerId: string, searchQuery: string) {
        this.layerFilters[layerId] = {
          ...this.layerFilters[layerId],
          legendFilters: [],
          searchQuery: searchQuery,
          source: ELayerFilterSource.Panel,
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
      setSelectedTimeSliderLayerId(selectedLayerId: string | null) {
        // Here, we reset the timeSlider values to prevent the timeSlider values from a previous layer from being carried over when selecting a new layer.
        // By passing the selectedLayerId, the selectedTimeSliderLayerId is also set at the same time.
        this.resetTimeSlider(selectedLayerId);
      },
      setTimeSliderDisplayMode(displayMode: ETimeSliderDisplayMode) {
        this.timeSliderDisplayMode = displayMode;
      },
      setTimeSliderStartDate(startDate: Date | null) {
        this.timeSliderStartDate = startDate;
      },
      setTimeSliderEndDate(endDate: Date | null) {
        this.timeSliderEndDate = endDate;
      },
      setTimeSliderStepSize(stepSize: ETimeSliderStepSize) {
        this.timeSliderStepSize = stepSize;
      },
      setTimeSliderCapabilitiesLoading(isLoading: boolean) {
        this.timeSliderCapabilitiesLoading = isLoading;
      },
      setTimeSliderCapabilitiesError(error: string | null) {
        this.timeSliderCapabilitiesError = error;
      },
      setTimeSliderDateRange(minDate: Date, maxDate: Date) {
        const startDate = cloneDate(minDate);
        const endDate = cloneDate(maxDate);

        this.timeSliderStartDate = startDate;
        this.timeSliderEndDate = endDate;
        this.timeSliderMinDate = cloneDate(minDate);
        this.timeSliderMaxDate = cloneDate(maxDate);
        this.timeSliderReferenceDate = cloneDate(startDate);
        this.timeSliderPeriodDates = [cloneDate(startDate), cloneDate(endDate)];
        this.timeSliderCapabilitiesError = null;
      },
      async loadTimeSliderCapabilitiesRange(layer: ILayer, user: IUser | null) {
        if (layer.source_type !== ELayerTypes.WMS && layer.source_type !== ELayerTypes.WMS_WFS) {
          this.setTimeSliderCapabilitiesError("De geselecteerde laag ondersteunt geen tijdslider metadata.");
          return;
        }

        this.setTimeSliderCapabilitiesLoading(true);
        this.setTimeSliderCapabilitiesError(null);

        try {
          const range = await getLayerTimeRange(layer, getFetchParameters(layer, user));

          if (this.selectedTimeSliderLayerId !== layer.id) {
            return;
          }

          if (!range) {
            this.setTimeSliderCapabilitiesError("Geen bruikbaar tijdslider bereik gevonden in tijdslider metadata.");
            return;
          }

          this.setTimeSliderDateRange(range.minDate, range.maxDate);
        } catch (error) {
          if (this.selectedTimeSliderLayerId !== layer.id) {
            return;
          }

          this.setTimeSliderCapabilitiesError(
            error instanceof Error ? error.message : "Tijdslider metadata kon niet gelezen worden.",
          );
        } finally {
          if (this.selectedTimeSliderLayerId === layer.id) {
            this.setTimeSliderCapabilitiesLoading(false);
          }
        }
      },
      setTimeSliderReferenceDate(referenceDate: Date) {
        this.timeSliderReferenceDate = referenceDate;
      },
      setTimeSliderPeriodDates(periodDates: [Date, Date]) {
        this.timeSliderPeriodDates = periodDates;
      },
      resetTimeSlider(selectedLayerId: string | null = null) {
        const selectedLayer = this.layers.find((layer) => layer.id === selectedLayerId);

        this.selectedTimeSliderLayerId = selectedLayerId;
        this.timeSliderDisplayMode = getLayerDefaultTimeSliderDisplayMode(selectedLayer);
        this.timeSliderStartDate = null;
        this.timeSliderEndDate = null;
        this.timeSliderMinDate = null;
        this.timeSliderMaxDate = null;
        this.timeSliderCapabilitiesLoading = false;
        this.timeSliderCapabilitiesError = null;
        this.timeSliderStepSize = ETimeSliderStepSize.Year;
        this.timeSliderReferenceDate = createDefaultTimeSliderStartDate();
        this.timeSliderPeriodDates = [createDefaultTimeSliderStartDate(), createDefaultTimeSliderEndDate()];
      },
      toggleTimeSliderPanel() {
        if (!this.timeSlider) {
          this.timeSlider = true;
        }

        this.showTimeSliderPanel = !this.showTimeSliderPanel;
      },
      closeTimeSliderPanel() {
        this.showTimeSliderPanel = false;
      },
      disableTimeSlider() {
        const selectedTimeSliderLayerId = this.selectedTimeSliderLayerId;

        if (selectedTimeSliderLayerId) {
          this.updateLayer(selectedTimeSliderLayerId, (layer) => {
            layer.is_visible = false;
          });
        }

        this.resetTimeSlider();
        this.showTimeSliderPanel = false;
        this.timeSlider = false;
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
      activateVisibleTimeSliderLayer() {
        const selectedLayer = this.layers.find((layer) => layer.is_visible && !layer.is_base && layer.is_time_enabled);

        if (!selectedLayer) {
          return;
        }

        this.toggleLayer({
          selectedLayerId: selectedLayer.id,
          is_visible: true,
        });
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
      toggleBaseLayer(selectedLayerProps: IToggleLayerProps) {
        const layer = this.layers.find((l) => l.id === selectedLayerProps.selectedLayerId);

        if (layer) {
          layer.is_visible = selectedLayerProps.is_visible;

          if (this.selectedBaseLayer) {
            this.selectedBaseLayer.is_visible = false;
          }
          this.selectedBaseLayer = layer;
        }
      },
      toggleLayer(selectedLayerProps: IToggleLayerProps) {
        const selectedLayer = this.layers.find((layer) => layer.id === selectedLayerProps.selectedLayerId);

        // Time-enabled layers are mutually exclusive because the time slider can target only one layer at a time.
        if (selectedLayer?.is_time_enabled) {
          if (!selectedLayerProps.is_visible) {
            this.updateLayer(selectedLayerProps.selectedLayerId, (layer) => {
              layer.is_visible = false;
            });

            // Only reset the slider when the currently targeted time-enabled layer is deselected.
            if (this.selectedTimeSliderLayerId === selectedLayerProps.selectedLayerId) {
              this.resetTimeSlider();
              this.showTimeSliderPanel = false;
              this.timeSlider = false;
            }

            this.resetFiltersForLayer(selectedLayerProps.selectedLayerId);
            return;
          }

          this.layers.forEach((layer) => {
            if (!layer.is_time_enabled || layer.id === selectedLayerProps.selectedLayerId) {
              return;
            }

            this.updateLayer(layer.id, (timeEnabledLayer) => {
              timeEnabledLayer.is_visible = false;
            });

            this.resetFiltersForLayer(layer.id);
          });

          this.updateLayer(selectedLayerProps.selectedLayerId, (layer) => {
            layer.is_visible = true;
          });

          this.resetTimeSlider(selectedLayerProps.selectedLayerId);
          this.timeSlider = true;
          this.showTimeSliderPanel = true;
          this.resetFiltersForLayer(selectedLayerProps.selectedLayerId);
          return;
        }

        this.updateLayer(selectedLayerProps.selectedLayerId, (layer) => {
          layer.is_visible = selectedLayerProps.is_visible;
        });

        this.resetFiltersForLayer(selectedLayerProps.selectedLayerId);
      },
      setLayerOpacity(selectedLayerProps: ISetLayerOpacityProps) {
        this.updateLayer(selectedLayerProps.selectedLayerId, (layer) => {
          layer.opacity = selectedLayerProps.opacity;
        });
      },
      toggleLayerisSelectable(selectedLayerProps: IToggleLayerSelectableProps) {
        this.updateLayer(selectedLayerProps.selectedLayerId, (layer) => {
          layer.is_selectable = selectedLayerProps.is_selectable;
        });
      },
      setDrawingId(drawingId: string) {
        this.drawingId = drawingId;
      },
      changeLayerOrder(layerOrderDetails: ILayerOrderDetails) {
        const layerId = layerOrderDetails.selectedLayerId;
        const direction = layerOrderDetails.direction;

        const index = this.layers.findIndex((layer) => layer.id === layerId);
        const visibleLayerIndex = this.visibleLayers.findIndex((layer) => layer.id === layerId);

        if (index === -1 || visibleLayerIndex === -1) {
          console.warn(`Layer with ID ${layerId} not found`);
          return;
        }

        if (
          (direction === "down" && visibleLayerIndex >= this.visibleLayers.length - 1) ||
          (direction === "up" && visibleLayerIndex <= 0)
        ) {
          return;
        }

        // Target the adjacent visible layer
        const newVisibleLayerIndex = direction === "down" ? visibleLayerIndex + 1 : visibleLayerIndex - 1;

        const layerToSwapWith = this.visibleLayers[newVisibleLayerIndex];
        const swapWithIndex = this.layers.findIndex((layer) => layer.id === layerToSwapWith.id);
        const layerToMove = this.layers[index];

        // Copy layers and perform reorder
        const newLayers = [...this.layers];
        newLayers.splice(index, 1);
        newLayers.splice(swapWithIndex, 0, layerToMove);

        this.setLayers(newLayers);
      },
    },
    getters: {
      getActiveLayersWithFilterCount(state) {
        const activeFilters = Object.entries(state.layerFilters).filter(
          ([, layer]) =>
            Object.values(layer.filters || {}).some((filterArray) => filterArray.length > 0) ||
            (layer.legendFilters || []).length > 0 ||
            (layer.searchQuery && layer.searchQuery.trim() !== ""),
        );

        const count = activeFilters.reduce((totalCount, [, { filters, legendFilters, searchQuery }]) => {
          const hasActiveFilters = filters ? Object.values(filters).some((array) => array.length > 0) : false;
          const hasLegendFilters = legendFilters ? legendFilters.length > 0 : false;
          const hasSearchQuery = searchQuery && searchQuery.trim() !== "";
          const activeCount = hasActiveFilters || hasLegendFilters || hasSearchQuery ? 1 : 0;
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

          if (layerFilter.legendFilters && layerFilter.legendFilters.length > 0) {
            filterCount += layerFilter.legendFilters.length;
          }

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
        return state.layers.filter((layer: ILayer) => layer.is_base);
      },
      regularLayers: (state) => {
        return state.layers.filter((layer: ILayer) => !layer.is_base);
      },
      wmsWfsLayers: (state) => {
        return state.layers.filter(
          (l: ILayer) => !l.is_base && (l.source_type === "WMS" || l.source_type === "WMS_WFS"),
        );
      },
      wmsWfsAndWMTSLayers: (state) => {
        return state.layers.filter(
          (l: ILayer) =>
            !l.is_base && (l.source_type === "WMS" || l.source_type === "WMS_WFS" || l.source_type === "WMTS"),
        );
      },
      visibleLayers: (state) => {
        return state.layers.filter((layer: ILayer) => layer.category && layer.is_visible && !layer.is_base);
      },
      visibleLayersForFeatures: (state) => {
        return state.layers.filter((layer: ILayer) => layer.is_selectable && !layer.is_base && layer.is_visible);
      },
      visibleLayersForDataPanel: (state) => {
        return state.layers.filter(
          (layer: ILayer) =>
            layer.is_visible &&
            !layer.is_base &&
            layer.show_in_detail_panel &&
            visibleSourceTypes.includes(layer.source_type),
        );
      },
      visibleLayersForDetailPanel: (state) => {
        return state.layers.filter(
          (layer: ILayer) => layer.is_visible && layer.show_in_detail_panel && !layer.is_base && layer.is_selectable,
        );
      },
      visibleLayersForTimeSliderPanel: (state) => {
        return state.layers.filter((layer: ILayer) => layer.is_visible && !layer.is_base && layer.is_time_enabled);
      },
    },
  })();
}
