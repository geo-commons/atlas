import { defineStore } from "pinia";
import { EEditLayerMode } from "@/types/map";

export interface IEditLayerStore {
  editLayerMode: EEditLayerMode;
}

export function useEditLayerStore() {
  return defineStore(`editLayerStore`, {
    state: (): IEditLayerStore => ({
      editLayerMode: EEditLayerMode.NONE,
    }),
    actions: {
      setEditLayerMode(editLayerMode: EEditLayerMode) {
        this.editLayerMode = editLayerMode;
      },
    },
    getters: {},
  })();
}
