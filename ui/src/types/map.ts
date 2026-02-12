export enum EditLayerMode {
  ADD = "ADD",
  EDIT = "EDIT",
  NONE = "NONE",
}

/**
 * Represents the current map position and view state.
 * Contains information about the map's zoom level, center coordinates,
 * marker position, geolocation, extent, and animation settings.
 */
export interface IPosition {
  /** The current zoom level of the map */
  zoom: number;
  /** The center coordinates of the map view as [x, y] */
  center: [number, number];
  /** The marker coordinates as [x, y] or null if no marker is set */
  marker: [number, number] | null;
  /** The geolocation coordinates as [x, y] or null if geolocation is not active */
  geolocation: [number, number] | null;
  /** The map extent as [minX, minY, maxX, maxY] representing the visible bounding box */
  extent: [number, number, number, number];
  /** Whether to fly to the position (used for navigation; typically reset to false after navigation) */
  flyTo: boolean;
  /** Whether to use fast animation (300ms vs 1500ms) for map movements */
  animateFast: boolean;
  /** Whether to animate map movements */
  animate: boolean;
}
