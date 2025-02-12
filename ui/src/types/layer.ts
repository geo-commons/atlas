export interface ILayer {
  id: string;
  name: string;
  title: string;
  url: string;
  source_type: ELayerTypes;
}

export type ILayerProperties = Array<{
  name: string;
  maxOccurs: number;
  minOccurs: number;
  nillable: boolean;
  type: string;
  localType: string;
}>;

export enum ELayerTypes {
  WFS = "WFS",
  WMS = "WMS",
  WMS_WFS = "WMS_WFS",
}
