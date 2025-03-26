import { defineStore } from "pinia";
import { EditLayerMode } from "@/types/map";
import { ILayer } from "@/types/layer";
import Feature from "ol/Feature";

export interface IEditLayerStore {
  editLayerMode: EditLayerMode;
  feature: any;
  visibleLayers: ILayer[];
  selectedLayer: ILayer | null;
  highlightedFeatureAndLayer: {
    feature: Feature;
    layer: ILayer;
  } | null;
}

export const useEditLayerStore = defineStore("editLayer", {
  state: (): IEditLayerStore => ({
    editLayerMode: EditLayerMode.NONE,
    feature: null,
    selectedLayer: null,
    visibleLayers: [],
    highlightedFeatureAndLayer: null,
  }),
  actions: {
    setEditLayerMode(editLayerMode: EditLayerMode) {
      this.editLayerMode = editLayerMode;
    },
    setFeature(feature: any) {
      this.feature = feature;
    },
    setSelectedLayer(selectedLayer: ILayer | null) {
      this.selectedLayer = selectedLayer;
    },
    setVisibleLayers(visibleLayers: ILayer[]) {
      this.visibleLayers = visibleLayers;
    },
    setHighlightedFeatureAndLayer(highlightedFeatureAndLayer: { feature: Feature; layer: ILayer } | null) {
      this.highlightedFeatureAndLayer = highlightedFeatureAndLayer;
    },
    resetFeature() {
      this.feature = null;
    },
  },
});
