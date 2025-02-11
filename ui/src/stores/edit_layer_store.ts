import { defineStore } from "pinia";
import { EEditLayerMode } from "@/types/map";

export interface IEditLayerStore {
  editLayerMode: EEditLayerMode;
  // TODO: find correct type
  feature: any;
}

export const useEditLayerStore = defineStore("editLayer", {
  state: (): IEditLayerStore => ({
    editLayerMode: EEditLayerMode.NONE,
    feature: null,
  }),
  actions: {
    setEditLayerMode(editLayerMode: EEditLayerMode) {
      this.editLayerMode = editLayerMode;
    },
    setFeature(feature: any) {
      this.feature = feature;
    },
    resetFeature() {
      this.feature = null;
    },
  },
});
