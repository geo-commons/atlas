import type { IPosition } from "@/types/map";

/**
 * default position test data.
 */
const defaultPosition: IPosition = {
  center: [0, 0],
  zoom: 1,
  marker: null,
  geolocation: null,
  extent: [0, 0, 0, 0],
  flyTo: false,
  animateFast: false,
  animate: false,
};

/**
 * Creates position test data.
 * @param overrides - Optional position values to override the defaults.
 * @returns The position test data.
 */
export const createPosition = (overrides: Partial<IPosition> = {}): IPosition => ({
  ...defaultPosition,
  ...overrides,
});
