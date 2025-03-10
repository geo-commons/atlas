// Map events
export enum MapEvents {
  SHOW_FORM = "show-form",
  UPDATE_ABOUT = "update-about",
  TOGGLE_ABOUT = "toggle-about",
}

// Common interfaces
export interface AboutFeatures {
  showAbout: boolean;
  showAboutButton: boolean;
  showAboutThumbnail: boolean;
}

// Map data interfaces
export interface MapAboutData {
  about: string | null;
  about_title: string | null;
  thumbnail?: string;
  features: AboutFeatures;
}

export interface AboutPanelData {
  features: AboutFeatures;
  about: string | null;
  aboutTitle: string | null;
  showPanel: boolean;
  thumbnail?: string;
}

// Event emit interfaces
export interface MapAboutEmits {
  (e: typeof MapEvents.SHOW_FORM): void;
  (e: typeof MapEvents.UPDATE_ABOUT, data: MapAboutData): void;
}

export interface AboutPanelEmits {
  (e: typeof MapEvents.TOGGLE_ABOUT): void;
}
