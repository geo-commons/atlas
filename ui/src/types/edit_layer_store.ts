import { EditLayerMode } from "@/types/map";
import Feature from "ol/Feature";
import { ILayer } from "@/types/layer";
import { GeometryType } from "ol/render/webgl/MixedGeometryBatch";

export interface IEditLayerStore {
  editLayerMode: EditLayerMode;
  feature: Feature | null;
  geometryType: GeometryType | null;
  visibleLayers: ILayer[];
  selectedLayer: ILayer | null;
  highlightedFeatureAndLayer: {
    feature: Feature;
    layer: ILayer;
  } | null;
}
