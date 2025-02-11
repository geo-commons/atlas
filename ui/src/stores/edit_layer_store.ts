import { defineStore } from "pinia";
import { EEditLayerMode } from "@/types/map";

export interface IEditLayerStore {
  editLayerMode: EEditLayerMode;
  // TODO: find correct type
  feature: any;
  // TODO: find correct type
  selectedLayer: any;
}

export const useEditLayerStore = defineStore("editLayer", {
  state: (): IEditLayerStore => ({
    editLayerMode: EEditLayerMode.NONE,
    feature: null,
    selectedLayer: null,
  }),
  actions: {
    setEditLayerMode(editLayerMode: EEditLayerMode) {
      this.editLayerMode = editLayerMode;
    },
    setFeature(feature: any) {
      this.feature = feature;
    },
    setSelectedLayer(selectedLayer: any) {
      this.selectedLayer = selectedLayer;
    },
    resetFeature() {
      this.feature = null;
    },
  },
});
