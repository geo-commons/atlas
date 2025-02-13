import { defineStore } from "pinia";
import { EEditLayerMode } from "@/types/map";
import { ILayer } from "@/types/layer";

export interface IEditLayerStore {
  editLayerMode: EEditLayerMode;
  feature: any;
  selectedLayer: ILayer | null;
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
    setSelectedLayer(selectedLayer: ILayer | null) {
      this.selectedLayer = selectedLayer;
    },
    resetFeature() {
      this.feature = null;
    },
  },
});
