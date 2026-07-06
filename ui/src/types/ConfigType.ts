export interface IConfigFeatures {
  portal?: boolean;
}

export interface IConfigPosition {
  center: { x: number; y: number };
  zoom: number;
}

export enum EComplexDataDisplay {
  PANEL = "panel",
  POPUP = "popup",
}
export interface IConfigStyle {
  complex_data_display: EComplexDataDisplay;
}
export interface IConfig {
  features: IConfigFeatures;
  position?: IConfigPosition;
  organization_logo?: string;
  organization_name?: string;
  organization_header?: string;
  organization_introduction?: string;
  organization_image?: string;
  organization_primary_color?: string;
  organization_title_color?: string;
  organization_text_color?: string;
  style: IConfigStyle;
}
