import GeoJSON from "ol/format/GeoJSON";
import { getCenter } from "ol/extent";

/**
 * A helper function to determine the center point of the selected feature.
 * Note: since the center point is not always contained within the feature itself, it is required to check
 * if this is the case. This is to prevent a situation where a marker might be placed outside a selected feature.
 *
 * @param feature
 * @returns Coordinates of the center point of the selected feature
 */
export function getFeatureCenterCoordinates(feature) {
  const geometry = new GeoJSON().readFeature(feature).getGeometry();
  const geometryExtend = geometry.getExtent();
  const center = getCenter(geometryExtend);

  // Check if the center is within the geometry of the selected feature.
  // Otherwise we choose the closest point to the center within the geometry.
  return geometry.containsXY(center[0], center[1])
    ? center
    : geometry.getClosestPoint(center);
}
