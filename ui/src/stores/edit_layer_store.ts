import { defineStore } from "pinia";
import { EditLayerMode } from "@/types/map";
import { ILayer } from "@/types/layer";
import Feature from "ol/Feature";
import { IEditLayerStore } from "@/types/edit_layer_store";
import { GeometryType } from "ol/render/webgl/MixedGeometryBatch";

export const useEditLayerStore = defineStore("editLayer", {
  state: (): IEditLayerStore => ({
    editLayerMode: EditLayerMode.NONE,
    feature: null,
    selectedLayer: null,
    geometryType: null,
    visibleLayers: [],
    highlightedFeatureAndLayer: null,
  }),
  actions: {
    setEditLayerMode(editLayerMode: EditLayerMode) {
      this.editLayerMode = editLayerMode;
    },
    setFeature(feature: Feature) {
      this.feature = feature;
    },
    setSelectedLayer(selectedLayer: ILayer | null) {
      this.selectedLayer = selectedLayer;
    },
    setGeometryType(geometryType: GeometryType | null) {
      this.geometryType = geometryType;
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
  getters: {
    isEditLayerModeNone(state) {
      return state.editLayerMode === EditLayerMode.NONE;
    },
  },
});
