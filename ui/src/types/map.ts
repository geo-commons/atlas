export enum EditLayerMode {
  ADD = "ADD",
  EDIT = "EDIT",
  NONE = "NONE",
}

export interface IPosition {
  center: [number, number];
  zoom: number;
}
