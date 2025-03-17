export interface ILayer {
  id: string;
  name: string;
  title: string;
  url: string;
  source_type: ELayerTypes;
  is_visible: boolean;
  projection: string;
}

export type ILayerProperties = Array<{
  name: string;
  maxOccurs: number;
  minOccurs: number;
  nillable: boolean;
  type: string;
  localType: string;
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
