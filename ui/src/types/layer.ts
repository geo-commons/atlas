import { GeometryType } from "ol/render/webgl/MixedGeometryBatch";
import type { ETimeSliderDisplayMode } from "@/types/mapStore";
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
  disable_highlighted_style: boolean;
  is_base: boolean;
  category: any;
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
  extent: [number, number, number, number] | null;
  zoom_min: number | null;
  zoom_max: number | null;
  is_time_enabled: boolean;
  is_reference_date_enabled: boolean;
  time_slider_default_display_mode: ETimeSliderDisplayMode;
  time_slider_start_field: string | null;
  time_slider_end_field: string | null;
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

type SelectedLayerId = {
  selectedLayerId: string;
};

export type IToggleLayerProps = SelectedLayerId & {
  is_visible: boolean;
};

export type ISetLayerOpacityProps = SelectedLayerId & {
  opacity: number;
};

export type IToggleLayerSelectableProps = SelectedLayerId & {
  is_selectable: boolean;
};
export interface ILayerOrderDetails {
  selectedLayerId: string;
  direction: string;
}
