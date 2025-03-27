import { EditLayerMode } from "@/types/map";
import Feature from "ol/Feature";
import { ILayer } from "@/types/layer";

export interface IEditLayerStore {
  editLayerMode: EditLayerMode;
  feature: Feature | null;
  visibleLayers: ILayer[];
  selectedLayer: ILayer | null;
  highlightedFeatureAndLayer: {
    feature: Feature;
    layer: ILayer;
  } | null;
}
