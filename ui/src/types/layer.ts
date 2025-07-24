import { GeometryType } from "ol/render/webgl/MixedGeometryBatch";

export interface ILayer {
  id: string;
  name: string;
  title: string;
  url: string;
  source_type: ELayerTypes;
  is_visible: boolean;
  projection: string;
  can_write: boolean;
  opacity: number;
  is_selectable: boolean;
  is_base: boolean;
  category: string;
  show_in_detail_panel: boolean;
}

export type IGeometryType = GeometryType | "Geometry";

export type ILayerProperties = Array<{
  name: string;
  maxOccurs: number;
  minOccurs: number;
  nillable: boolean;
  type: string;
  localType: IGeometryType;
}>;

export type IFeatureProperties = {
  targetNamespace: string;
  targetPrefix: string;
};

export enum ELayerTypes {
  WFS = "WFS",
  WMS = "WMS",
  WMS_WFS = "WMS_WFS",
}

export interface ISelectedLayerProps {
  selectedLayerId: string;
  is_visible: boolean;
  opacity: number;
  is_selectable: boolean;
}

export interface ILayerOrderDetails {
  selectedLayerId: string;
  direction: string;
}
