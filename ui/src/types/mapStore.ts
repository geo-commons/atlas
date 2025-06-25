export interface ILayerFilter {
  filters: {
    [key: string]: Array<string>;
  };
  searchQuery: string;
}

export interface ICycloView {
  detail: {
    yaw: number;
    pitch: number;
    hFov: number;
  };
}

export interface ILayerFilters {
  // key is layer id
  [key: string]: ILayerFilter;
}

export interface IMapStore {
  layerFilters: ILayerFilters;
  leftSelectedCompareLayerId: string | null;
  rightSelectedCompareLayerId: string | null;
  comparePercentage: number;
  cycloView: ICycloView | null;
}
