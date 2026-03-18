import { EditLayerMode } from "@/types/map";
import Feature from "ol/Feature";
import { IGeometryType, ILayer } from "@/types/layer";

export interface IEditLayerStore {
  editLayerMode: EditLayerMode;
  feature: Feature | null;
  draftFeature: Feature | null;
  modifiedFeature: Feature | null;
  editableLayers: ILayer[];
  geometryType: IGeometryType | null;
  selectedLayer: ILayer | null;
  hideOtherPanels: boolean;
  isDrawingFeaturePart: boolean;
  isRedrawingFeature: boolean;
  highlightedFeatureAndLayer: {
    feature: Feature;
    layer: ILayer;
  } | null;
}
