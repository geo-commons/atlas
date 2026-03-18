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
    draftFeature: null,
    modifiedFeature: null,
    selectedLayer: null,
    geometryType: null,
    editableLayers: [],
    highlightedFeatureAndLayer: null,
    hideOtherPanels: false,
    isDrawingFeaturePart: false,
    isRedrawingFeature: false,
  }),
  actions: {
    setEditLayerMode(editLayerMode: EditLayerMode) {
      this.editLayerMode = editLayerMode;
    },
    setFeature(feature: Feature) {
      this.feature = feature;
    },
    setDraftFeature(draftFeature: Feature | null) {
      // Stores a multipart feature while the user is still adding parts.
      this.draftFeature = draftFeature;
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
    setIsDrawingFeaturePart(isDrawingFeaturePart: boolean) {
      // Tracks whether the current MultiPoint/MultiLineString/MultiPolygon part is still being drawn.
      this.isDrawingFeaturePart = isDrawingFeaturePart;
    },
    setIsRedrawingFeature(isRedrawingFeature: boolean) {
      this.isRedrawingFeature = isRedrawingFeature;
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
      this.draftFeature = null;
      this.modifiedFeature = null;
      this.isDrawingFeaturePart = false;
      this.isRedrawingFeature = false;
    },
    resetEditLayerProperties() {
      this.editLayerMode = EditLayerMode.NONE;
      this.feature = null;
      this.draftFeature = null;
      this.modifiedFeature = null;
      this.geometryType = null;
      this.selectedLayer = null;
      this.highlightedFeatureAndLayer = null;
      this.hideOtherPanels = false;
      this.isDrawingFeaturePart = false;
      this.isRedrawingFeature = false;
    },
  },
  getters: {
    isEditLayerModeNone(state) {
      return state.editLayerMode === EditLayerMode.NONE;
    },
  },
});
