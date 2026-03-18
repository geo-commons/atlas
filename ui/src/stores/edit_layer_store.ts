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
    modifiedFeature: null,
    selectedLayer: null,
    geometryType: null,
    editableLayers: [],
    highlightedFeatureAndLayer: null,
    hideOtherPanels: false,
  }),
  actions: {
    setEditLayerMode(editLayerMode: EditLayerMode) {
      this.editLayerMode = editLayerMode;
    },
    setFeature(feature: Feature) {
      this.feature = feature;
    },
    setModifiedFeature(modifiedFeature: Feature) {
      this.modifiedFeature = modifiedFeature;
    },
    toggleHideOtherPanels() {
      this.hideOtherPanels = !this.hideOtherPanels;
    },
    setSelectedLayer(selectedLayer: ILayer | null) {
      this.selectedLayer = selectedLayer;
    },
    setGeometryType(geometryType: GeometryType | null) {
      this.geometryType = geometryType;
    },
    setEditableLayers(editableLayers: ILayer[]) {
      this.editableLayers = editableLayers;
    },
    setHighlightedFeatureAndLayer(highlightedFeatureAndLayer: { feature: Feature; layer: ILayer } | null) {
      this.highlightedFeatureAndLayer = highlightedFeatureAndLayer;
      this.modifiedFeature = highlightedFeatureAndLayer ? highlightedFeatureAndLayer.feature : null;
    },
    resetFeature() {
      this.feature = null;
      this.modifiedFeature = null;
    },
    resetEditLayerProperties() {
      this.editLayerMode = EditLayerMode.NONE;
      this.feature = null;
      this.modifiedFeature = null;
      this.geometryType = null;
      this.selectedLayer = null;
      this.highlightedFeatureAndLayer = null;
      this.hideOtherPanels = false;
    },
  },
  getters: {
    isEditLayerModeNone(state) {
      return state.editLayerMode === EditLayerMode.NONE;
    },
  },
});
