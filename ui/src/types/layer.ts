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
