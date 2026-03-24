import { GeometryType } from "ol/render/webgl/MixedGeometryBatch";
import { IMetadataset } from "./metadataset";

export interface ILayer {
  id: string;
  name: string;
  title: string;
  description?: string;
  url: string;
  source_type: ELayerTypes;
  is_visible: boolean;
  projection: string;
  can_write: boolean;
  opacity: number;
  friendly_fields: { [key: string]: string };
  is_selectable: boolean;
  is_base: boolean;
  category: string;
  show_in_detail_panel: boolean;
  metadataset?: IMetadataset | null;
  metadata?: {
    description: string;
    lineage: string;
    organization: string;
    contact: string;
    updated: string;
    link: string;
  };
  server_type: string;
  server_style: string | null;
  source: {
    authenticate: boolean;
  };
  login_required: boolean;
}

export type IGeometryType = GeometryType | "Geometry";

export type IGeoserverType = IGeometryType | "boolean" | "date" | "number" | "int" | "string" | "time" | "date-time";

export type ILayerProperties = Array<{
  name: string;
  maxOccurs: number;
  minOccurs: number;
  nillable: boolean;
  type: string;
  localType: IGeoserverType;
  restriction?: {
    minInclusive?: number;
    maxInclusive?: number;
    enumeration?: string[] | number[];
  };
}>;

export type IFeatureProperties = {
  targetNamespace: string;
  targetPrefix: string;
};

export enum ELayerTypes {
  WFS = "WFS",
  WMS = "WMS",
  WMS_WFS = "WMS_WFS",
  WMTS = "WMTS",
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
